import os
import struct

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# AU file header format:
#  0 -  3: Magic number ".snd"
#  4 -  7: Data offset (32 bytes for this example)
#  8 - 11: Data size (0xFFFFFFFF for unknown size)
# 12 - 15: Encoding (1 for μ-law 8-bit samples)
# 16 - 19: Sample rate (e.g., 8000 Hz)
# 20 - 23: Channels (e.g., 1 for mono)
# 24 - 31: Optional textual information (padded to 8 bytes)

def create_au_file(filename, sample_rate=8000, channels=1):
    # AU header parameters
    magic_number = b'.snd'
    data_offset = 32  # bytes
    data_size = 0xFFFFFFFF  # unknown size
    encoding = 1  # μ-law 8-bit samples
    
    # Create header
    header = struct.pack('>4s5I8s',
                         magic_number,
                         data_offset,
                         data_size,
                         encoding,
                         sample_rate,
                         channels,
                         b'Metadata')  # 8 bytes of textual info

    # Example audio data (silence, μ-law encoded)
    audio_data = bytes([0xFF] * 8000)  # 1 second of silence

    # Write to file
    with open(filename, 'wb') as f:
        f.write(header)
        f.write(audio_data)

# Generate AU file
create_au_file(os.path.join(output_dir, 'example.au'))