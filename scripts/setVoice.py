import json
import os
from pathlib import Path
import sys

# Check if both arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <name_to_find> <voice_model_id>")
    sys.exit(1)

# Get arguments from command line
name_to_find = sys.argv[1]
voice_model_id = sys.argv[2]

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Find and process JSON file with matching name
found = False
for json_file in Path(modes_dir).glob('*.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if data.get('name') == name_to_find:
            # Update voiceModelID
            data['voiceModelID'] = voice_model_id
            
            # Set language based on voice model ID
            if voice_model_id == "sw-deepgram-nova-2":
                data['language'] = "multi"
            else:
                data['language'] = "auto"
            
            # Write back the modified content
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Updated file: {json_file}")
            found = True
            break

if not found:
    print(f"No JSON file found with name: {name_to_find}")