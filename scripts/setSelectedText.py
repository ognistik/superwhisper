import json
import os
from pathlib import Path

# Define path
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Process all JSON files in the directory
updated_count = 0
for json_file in Path(modes_dir).glob('*.json'):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check if contextFromSelection exists and is not true
        if data.get('contextFromSelection') is not True:
            # Update the value
            data['contextFromSelection'] = True
            
            # Write back the modified content
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Updated file: {json_file}")
            updated_count += 1
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

print(f"Process complete. Updated {updated_count} files.")