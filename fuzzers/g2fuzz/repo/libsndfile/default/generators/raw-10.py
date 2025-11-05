import os
import numpy as np

# Ensure the directory exists
os.makedirs('./tmp', exist_ok=True)

# Define the dimensions of the sensor data (e.g., a 10x10 image sensor)
width, height = 10, 10

# Generate random sensor data to simulate a raw image
sensor_data = np.random.randint(0, 65536, (height, width), dtype=np.uint16)

# Save the raw sensor data to a file
file_path = './tmp/raw_image.raw'
sensor_data.tofile(file_path)

print(f"Raw file generated and saved to {file_path}")