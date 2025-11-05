import os
import numpy as np

# Ensure the directory exists
os.makedirs('./tmp', exist_ok=True)

# Define image dimensions
width, height = 100, 100

# Simulate a raw image data array (grayscale for simplicity)
# In a real raw file, this would be sensor data, usually in Bayer format
raw_image_data = np.random.randint(0, 65536, (height, width), dtype=np.uint16)

# Simulate metadata for white balance (using default 1.0 multipliers for simplicity)
# In a real scenario, these values would be used to adjust the red, green, and blue channels
metadata = {
    'white_balance': {
        'red_multiplier': 1.0,
        'green_multiplier': 1.0,
        'blue_multiplier': 1.0
    }
}

# Convert the metadata to a byte representation
metadata_bytes = str(metadata).encode('utf-8')

# Define the file path
file_path = './tmp/mock_raw_image.raw'

# Write the raw image data and metadata to a file
with open(file_path, 'wb') as file:
    # Write the image data
    file.write(raw_image_data.tobytes())
    # Write the metadata
    file.write(metadata_bytes)

print(f'Raw file generated at: {file_path}')