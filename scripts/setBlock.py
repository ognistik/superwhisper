import json
import os
from pathlib import Path
import sys

# Define tag mapping - single source of truth
tag_mapping = {
    "Style Guides": "style-guides",
    "Banned Words": "banned-words"
    # Add more mappings here as needed
}

# Check if arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script.py <tag_type> <new content>")
    print(f"Available tag types: {', '.join(tag_mapping.keys())}")
    sys.exit(1)

# Get arguments from command line
tag_type = sys.argv[1]
new_content = sys.argv[2]

# Validate first argument using the mapping
if tag_type not in tag_mapping:
    print(f"Error: First argument must be one of: {', '.join(tag_mapping.keys())}")
    sys.exit(1)

# Define paths
modes_dir = '/Users/ognistik/Documents/superwhisper/modes'

# Get tag name from mapping
tag_name = tag_mapping[tag_type]
start_tag = f"<{tag_name}>"
end_tag = f"</{tag_name}>"

# Counter for modified files
modified_count = 0

# Process all JSON files in the directory
for json_file in Path(modes_dir).glob('*.json'):
    try:
        # Read the file
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # Check if the file has a prompt field
                if 'prompt' in data:
                    prompt_content = data['prompt']
                    
                    # Check if the prompt contains the specified XML tags
                    start_index = prompt_content.find(start_tag)
                    end_index = prompt_content.find(end_tag)
                    
                    if start_index != -1 and end_index != -1:
                        # Replace the content between tags with a line break after opening tag only
                        new_prompt = (
                            prompt_content[:start_index + len(start_tag)] + 
                            "\n" + new_content + 
                            prompt_content[end_index:]
                        )
                        
                        # Update the prompt in the data
                        data['prompt'] = new_prompt
                        
                        # Write the updated data back to the file
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        
                        print(f"Updated file: {json_file}")
                        modified_count += 1
            
            except json.JSONDecodeError:
                print(f"Error: Could not parse JSON in file {json_file}")
                continue
    
    except Exception as e:
        print(f"Error processing file {json_file}: {str(e)}")

print(f"Process completed. Modified {modified_count} files.")