import os
import numpy as np

# Create a directory for storing raw files if it doesn't exist
os.makedirs('./tmp/', exist_ok=True)

# Function to generate a large RAW file
def generate_large_raw_file(filename, width, height, channels):
    """
    Generates a large 'RAW' like file with random data representing pixel values.
    The file is saved in the specified filename with the given dimensions.

    :param filename: The name of the file to be created.
    :param width: The width of the image (number of pixels).
    :param height: The height of the image (number of pixels).
    :param channels: The number of color channels (e.g., 3 for RGB).
    """
    # Calculate the size of the data in bytes
    size_in_bytes = width * height * channels

    # Generate random data to simulate raw pixel data
    data = np.random.randint(0, 256, size=size_in_bytes, dtype=np.uint8)

    # Save to a file
    with open(filename, 'wb') as file:
        file.write(data.tobytes())

# Parameters for the raw file (large size)
width = 5000   # Width of the image
height = 3000  # Height of the image
channels = 3   # RGB channels

# Generate and save the large raw file
generate_large_raw_file('./tmp/large_image.raw', width, height, channels)