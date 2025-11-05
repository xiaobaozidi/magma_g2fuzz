import os
import numpy as np
from PIL import Image

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

def generate_raw_file(filename, width, height):
    # Generate random image data
    data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # Save as a raw file (simulating a raw binary format)
    raw_path = os.path.join(output_dir, filename)
    with open(raw_path, 'wb') as f:
        f.write(data.tobytes())

def generate_lossless_compressed_file(filename, width, height):
    # Generate random image data
    data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # Save as a PNG file to ensure lossless compression
    img = Image.fromarray(data, 'RGB')
    compressed_path = os.path.join(output_dir, filename)
    img.save(compressed_path, format='PNG')

# Generate a raw file (simulated)
generate_raw_file('image.raw', 100, 100)

# Generate a losslessly compressed file (e.g., PNG)
generate_lossless_compressed_file('image.png', 100, 100)