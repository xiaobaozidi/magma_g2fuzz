import os
import json
import random

# Ensure the directory exists
os.makedirs('./tmp', exist_ok=True)

# Function to generate random metadata
def generate_metadata():
    metadata = {
        "camera_settings": {
            "aperture": f"f/{random.uniform(1.4, 22):.1f}",
            "shutter_speed": f"1/{random.randint(30, 8000)}s",
            "iso": random.choice([100, 200, 400, 800, 1600, 3200, 6400]),
        },
        "exposure_info": {
            "exposure_compensation": f"{random.uniform(-3, 3):.1f} EV",
            "white_balance": random.choice(["Auto", "Daylight", "Cloudy", "Tungsten", "Fluorescent"]),
        },
        "other_data": {
            "date_taken": "2023-10-10",
            "location": random.choice(["New York", "Paris", "Tokyo", "Sydney"]),
            "photographer": random.choice(["John Doe", "Jane Smith", "Alex Johnson"]),
        }
    }
    return metadata

# Generate and save 5 dummy RAW files
for i in range(1, 6):
    raw_data = os.urandom(1024 * 1024)  # 1MB of random raw data
    metadata = generate_metadata()
    
    # Save raw data
    raw_file_path = f'./tmp/image_{i}.raw'
    with open(raw_file_path, 'wb') as raw_file:
        raw_file.write(raw_data)
    
    # Save metadata as a JSON file
    metadata_file_path = f'./tmp/image_{i}_metadata.json'
    with open(metadata_file_path, 'w') as metadata_file:
        json.dump(metadata, metadata_file, indent=4)