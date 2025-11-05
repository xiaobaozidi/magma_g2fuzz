import os
import struct

# Directory to save the AU files
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Function to create an AU file with a simple header
def create_au_file(filename, sample_rate=8000, channels=1, encoding_format=1, data=b''):
    """
    Create an AU file with a simple header.

    :param filename: Name of the file to be created.
    :param sample_rate: Sample rate of the audio.
    :param channels: Number of audio channels.
    :param encoding_format: Encoding format (1 for 8-bit μ-law, 2 for 8-bit linear PCM, etc.).
    :param data: Audio data to be written.
    """
    # AU file header fields
    magic_number = b'.snd'  # AU file magic number
    offset = 24  # Header size
    data_size = len(data)  # Size of the audio data
    header = struct.pack(
        '>4s5I',     # Big-endian: 4-byte string and 5 integers
        magic_number,
        offset,
        data_size,
        encoding_format,
        sample_rate,
        channels
    )

    # Write header and data to file
    with open(os.path.join(output_dir, filename), 'wb') as au_file:
        au_file.write(header)  # Write header
        au_file.write(data)    # Write audio data

# Example usage: Create a simple AU file with silence (empty data)
create_au_file('example.au')

print(f"AU file created in {output_dir}")