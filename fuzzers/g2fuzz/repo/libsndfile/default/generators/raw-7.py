import os

# Directory for saving the files
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define some example RAW file content
content = b"This is a simulated RAW file content."

# Define some proprietary RAW file extensions
raw_formats = {
    'Canon': 'CR2',
    'Nikon': 'NEF',
    'Sony': 'ARW',
}

# Generate and save the RAW files
for brand, extension in raw_formats.items():
    file_path = os.path.join(output_dir, f'sample_{brand}.{extension}')
    with open(file_path, 'wb') as file:
        file.write(content)

print(f"RAW files have been generated and saved in {output_dir}")