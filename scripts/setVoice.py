import json
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
modes_dir = "/Users/ognistik/Documents/superwhisper/modes"

# Models that should force realtimeOutput = True
REALTIME_MODELS = {
    "nvidia_parakeet-v3_494MB",
    "sw-elevenlabs-scribe",
    "sw-deepgram-nova-3",
}

found = False

for json_file in Path(modes_dir).glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("name") == name_to_find:
        # Update voiceModelID
        data["voiceModelID"] = voice_model_id

        # Set language based on voice model ID
        if voice_model_id == "sw-deepgram-nova-3":
            data["language"] = "multi"
        else:
            data["language"] = "auto"

        # Set realtimeOutput based on voice model ID
        data["realtimeOutput"] = voice_model_id in REALTIME_MODELS

        # Write back the modified content
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Updated file: {json_file}")
        print(f"  voiceModelID: {data['voiceModelID']}")
        print(f"  language: {data['language']}")
        print(f"  realtimeOutput: {data['realtimeOutput']}")
        found = True
        break

if not found:
    print(f"No JSON file found with name: {name_to_find}")