import json
import os
from pathlib import Path
import sys

# Check if argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <name_to_find>")
    sys.exit(1)

# Get name from command line
name_to_find = sys.argv[1]

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Find and read JSON file with matching name
found = False
for json_file in Path(modes_dir).glob('*.json'):
    with open(json_file, 'r') as f:
        data = json.load(f)
        if data.get('name') == name_to_find:
            print(data['voiceModelID'])
            found = True
            break

if not found:
    print(f"No JSON file found with name: {name_to_find}")