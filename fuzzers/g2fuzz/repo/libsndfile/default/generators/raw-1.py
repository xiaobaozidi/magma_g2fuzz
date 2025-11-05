import os
import numpy as np
from PIL import Image

def create_raw_file(filename, width, height, bit_depth):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Generate random pixel data for a single channel
    max_value = 2 ** bit_depth - 1
    data = np.random.randint(0, max_value, (height, width), dtype=np.uint16)
    
    # Save the data as a 16-bit grayscale image, which simulates a raw-like file
    image = Image.fromarray(data, mode='I;16')
    image.save(filename)

# Parameters for the simulated RAW file
width = 256
height = 256
bit_depth = 16  # High bit depth

# Create a simulated RAW file
create_raw_file('./tmp/simulated_raw_file.png', width, height, bit_depth)