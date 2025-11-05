import numpy as np
import os

def generate_wide_dynamic_range_raw(width, height, filepath):
    """
    Generate a RAW file with wide dynamic range characteristics.

    :param width: Width of the image.
    :param height: Height of the image.
    :param filepath: Path where the RAW file will be saved.
    """
    # Simulate wide dynamic range by creating a gradient image with 16-bit depth
    # The gradient will extend from very dark (0) to very bright (65535)
    gradient = np.linspace(0, 65535, width, dtype=np.uint16)
    
    # Create an image with the gradient repeated across all rows
    image = np.tile(gradient, (height, 1))

    # Save the image as a binary RAW file
    with open(filepath, 'wb') as raw_file:
        image.tofile(raw_file)

# Directory to save the RAW files
output_dir = "./tmp/"
os.makedirs(output_dir, exist_ok=True)

# Parameters for the RAW image
image_width = 1024  # Width of the image
image_height = 1024  # Height of the image

# Path to save the RAW file
output_file = os.path.join(output_dir, "wide_dynamic_range.raw")

# Generate the RAW file
generate_wide_dynamic_range_raw(image_width, image_height, output_file)