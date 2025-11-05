import os
import random
import struct

# Ensure the ./tmp/ directory exists
os.makedirs('./tmp/', exist_ok=True)

# Generate a random "RAW" file with some arbitrary binary data
def generate_raw_file(filename):
    # Create a file path
    file_path = os.path.join('./tmp/', filename)

    # Open the file in binary write mode
    with open(file_path, 'wb') as f:
        # Write some arbitrary binary data
        # Here we simulate a RAW file with random bytes
        for _ in range(1024):  # Adjust the size as needed
            # Write a random byte
            f.write(struct.pack('B', random.randint(0, 255)))

# Generate a few RAW files
raw_file_names = ['file1.raw', 'file2.raw', 'file3.raw']
for raw_file_name in raw_file_names:
    generate_raw_file(raw_file_name)

print("RAW files generated in ./tmp/:", raw_file_names)