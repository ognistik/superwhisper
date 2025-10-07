import json
import os
import subprocess
import sys
from pathlib import Path

# Check if argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <name_to_find>")
    sys.exit(1)

# Get name from command line
name_to_find = sys.argv[1]

# Define paths
modes_dir = Path('~/Documents/superwhisper/modes').expanduser()

# Find JSON file with matching name and open it directly
found = False
for json_file in Path(modes_dir).glob('*.json'):
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
            if data.get('name') == name_to_find:
                # Open the file directly (not just reveal in Finder)
                subprocess.run(['open', str(json_file)])
                print(f"Opened file: {json_file}")
                found = True
                break
        except json.JSONDecodeError:
            print(f"Error: Could not parse {json_file} as JSON")
            continue

if not found:
    print(f"No JSON file found with name: {name_to_find}")