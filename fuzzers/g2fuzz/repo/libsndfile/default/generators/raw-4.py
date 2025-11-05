import os
import numpy as np

# Define the directory where the raw files will be saved
output_directory = './tmp/'
os.makedirs(output_directory, exist_ok=True)

# Define a function to generate raw sensor data
def generate_raw_data(width, height):
    # Simulate raw sensor data as a 2D array of integers
    # Assuming a 12-bit sensor, values range from 0 to 4095
    return np.random.randint(0, 4096, (height, width), dtype=np.uint16)

# Define the number of raw files to generate and their dimensions
num_files = 5
image_width = 4000  # Example width of a sensor in pixels
image_height = 3000  # Example height of a sensor in pixels

# Generate and save raw files
for i in range(num_files):
    raw_data = generate_raw_data(image_width, image_height)
    filename = os.path.join(output_directory, f'raw_data_{i+1}.bin')
    raw_data.tofile(filename)

print(f'{num_files} raw files have been generated and saved in {output_directory}')