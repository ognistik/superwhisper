import json
import os
from pathlib import Path
import sys

# Check if argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <tag_name>")
    sys.exit(1)

# Get argument from command line
arg = sys.argv[1]

# Define a mapping of user-friendly names to XML tag names
tag_mapping = {
    "Style Guides": "style-guides",
    "Banned Words": "banned-words"
    # Add more mappings here as needed
}

# Validate argument
if arg not in tag_mapping:
    print(f"Error: Argument must be one of: {', '.join(tag_mapping.keys())}")
    sys.exit(1)

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Get the corresponding XML tag
tag_to_find = tag_mapping[arg]

# Find and read JSON file with matching key
found = False
for json_file in Path(modes_dir).glob('*.json'):
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
            if data.get('key') == "custom-YYQY":
                prompt_content = data.get('prompt', '')
                
                # Extract content between XML tags
                start_tag = f"<{tag_to_find}>"
                end_tag = f"</{tag_to_find}>"
                
                start_index = prompt_content.find(start_tag)
                end_index = prompt_content.find(end_tag)
                
                if start_index != -1 and end_index != -1:
                    # Extract the content between tags
                    content = prompt_content[start_index + len(start_tag):end_index].strip()
                    print(content)
                    found = True
                    break
                else:
                    print(f"No {tag_to_find} tags found in the prompt")
                    found = True
                    break
        except json.JSONDecodeError:
            continue

if not found:
    print(f"No JSON file found with key: custom-YYQY")