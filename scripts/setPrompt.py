import json
import os
from pathlib import Path
import sys

# Check if both arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <name_to_find> <prompt_value>")
    sys.exit(1)

# Get arguments from command line
name_to_find = sys.argv[1]
prompt_value = sys.argv[2].strip()  # Strip leading/trailing whitespace

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Find and process JSON file with matching name
found = False
for json_file in Path(modes_dir).glob('*.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if data.get('name') == name_to_find:
            # Update prompt
            data['prompt'] = prompt_value
            
            # Write back the modified content with ensure_ascii=False
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Updated file: {json_file}")
            found = True
            break

if not found:
    print(f"No JSON file found with name: {name_to_find}")