#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

# ---------- CONFIG ----------
# Superwhisper modes JSON dir
MODES_DIR = '/Users/ognistik/Documents/superwhisper/modes'
# Alter prompts dir
ALTER_DIR = '/Users/ognistik/Alter Prompts'

# Mapping visible names -> XML tag names
TAG_MAPPING = {
    "Style Guides": "style-guides",
    "Banned Words": "banned-words",
    # add more here as needed
}
# ----------------------------

def usage():
    print("Usage:")
    print("  python setBlock.py <tag_type> <new_content|@/path/to/textfile>")
    print(f"  Available tag types: {', '.join(TAG_MAPPING.keys())}")
    sys.exit(1)

def read_new_content(arg: str) -> str:
    if arg.startswith('@'):
        path = arg[1:]
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return arg

def escape_for_double_quoted_yaml_scalar(s: str) -> str:
    # Preserve the file's style: a double-quoted scalar using explicit \n sequences
    # Escape backslashes and quotes, then convert real newlines to literal \n
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = s.replace('\n', '\\n')
    return s

def process_json_modes(tag_name: str, new_content_raw: str) -> int:
    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"
    modified = 0

    for json_file in Path(MODES_DIR).glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'prompt' not in data:
                continue

            prompt = data['prompt']
            s_idx = prompt.find(start_tag)
            e_idx = prompt.find(end_tag)
            if s_idx == -1 or e_idx == -1 or e_idx < s_idx:
                continue

            # Keep JSON behavior: insert a newline after opening tag and replace inner content
            updated = prompt[:s_idx + len(start_tag)] + "\n" + new_content_raw + prompt[e_idx:]
            if updated != prompt:
                data['prompt'] = updated
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"Updated JSON: {json_file}")
                modified += 1
        except Exception as e:
            print(f"Error JSON {json_file}: {e}")
    return modified

def find_top_level_system_double_quoted_block(text: str) -> tuple[int, int, int]:
    """
    Locate the double-quoted scalar for system: under prompt:.
    Returns (content_start_idx, content_end_idx, quote_open_idx)
    or (-1, -1, -1) if not found.
    """
    # Require 'prompt:' to appear before 'system:' to target the correct block
    p_pos = text.find('\nprompt:') if text.startswith('prompt:') is False else 0
    if p_pos == -1:
        # Maybe the file starts with 'prompt:' on first line
        p_pos = 0 if text.startswith('prompt:') else -1
    if p_pos == -1:
        return (-1, -1, -1)

    # Search for system: "<...>" after prompt:
    search_region = text[p_pos:]
    import re
    m = re.search(r'(?m)^[ \t]*system:[ \t]*"', search_region)
    if not m:
        return (-1, -1, -1)
    quote_open_in_region = m.end() - 1  # position of the opening double-quote
    quote_open = p_pos + quote_open_in_region
    i = quote_open + 1
    n = len(text)
    escaped = False
    while i < n:
        c = text[i]
        if escaped:
            escaped = False
        else:
            if c == '\\':
                escaped = True
            elif c == '"':
                # found closing quote
                content_start = quote_open + 1
                content_end = i
                return (content_start, content_end, quote_open)
        i += 1
    return (-1, -1, -1)

def process_alter_files(tag_name: str, new_content_raw: str) -> int:
    """
    Works on .alter (YAML-like) files that store system as a double-quoted scalar
    with literal '\n' sequences. No external YAML library required.
    """
    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"
    modified = 0

    for alter_file in Path(ALTER_DIR).glob('*.alter'):
        try:
            with open(alter_file, 'r', encoding='utf-8') as f:
                text = f.read()

            c_start, c_end, q_open = find_top_level_system_double_quoted_block(text)
            if c_start == -1:
                # Skip files not using the expected format
                continue

            system_content = text[c_start:c_end]  # content between the double quotes

            s_idx = system_content.find(start_tag)
            e_idx = system_content.find(end_tag)
            if s_idx == -1 or e_idx == -1 or e_idx < s_idx:
                continue

            # Maintain the file's style: use literal \n sequences inside the quoted scalar
            escaped_new_inner = escape_for_double_quoted_yaml_scalar(new_content_raw)
            replacement = "\\n" + escaped_new_inner  # keep behavior: newline after opening tag

            updated_system = (
                system_content[:s_idx + len(start_tag)]
                + replacement
                + system_content[e_idx:]
            )

            if updated_system != system_content:
                new_text = text[:c_start] + updated_system + text[c_end:]
                # Optional backup
                with open(alter_file.with_suffix(alter_file.suffix + '.bak'), 'w', encoding='utf-8') as bak:
                    bak.write(text)
                with open(alter_file, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                print(f"Updated ALTER: {alter_file}")
                modified += 1
        except Exception as e:
            print(f"Error ALTER {alter_file}: {e}")

    return modified

def main():
    if len(sys.argv) != 3:
        usage()

    tag_type = sys.argv[1]
    if tag_type not in TAG_MAPPING:
        print(f"Error: tag_type must be one of: {', '.join(TAG_MAPPING.keys())}")
        sys.exit(1)

    new_content_raw = read_new_content(sys.argv[2])
    tag_name = TAG_MAPPING[tag_type]

    total = 0
    total += process_json_modes(tag_name, new_content_raw)
    total += process_alter_files(tag_name, new_content_raw)

    print(f"Process completed. Modified {total} files.")

if __name__ == "__main__":
    main()