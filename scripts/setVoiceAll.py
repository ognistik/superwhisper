import json
import os
from pathlib import Path
import sys

# Check if argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <voice_model_id>")
    sys.exit(1)

# Get voice model ID from command line argument
voice_model_id = sys.argv[1]

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Process all JSON files
for json_file in Path(modes_dir).glob('*.json'):
    # Read and modify the file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data['voiceModelID'] = voice_model_id
        
        # Set language based on voice model ID
        if voice_model_id == "sw-deepgram-nova-3":
            data['language'] = "multi"
        else:
            data['language'] = "auto"
    
    # Write back the modified content with proper encoding
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

print("Modification complete")