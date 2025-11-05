import os
import numpy as np
import wave
import struct

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define parameters for the audio file
sample_rate = 8000  # 8 kHz
duration = 2        # 2 seconds
frequency = 440.0   # A4 note

# Generate audio data (a simple sine wave)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert the audio data to 16-bit PCM format
audio_data = np.int16(audio_data * 32767)

# Define AU file header parameters
magic_number = b".snd"
header_size = 24
audio_data_size = len(audio_data) * 2  # 2 bytes per sample for 16-bit PCM
encoding = 3  # 16-bit linear PCM
channels = 1
sample_rate = 8000

# Create the AU file
output_file = os.path.join(output_dir, 'example.au')
with open(output_file, 'wb') as au_file:
    # Write the AU header
    au_file.write(magic_number)
    au_file.write(struct.pack('>I', header_size))          # Header size
    au_file.write(struct.pack('>I', audio_data_size))      # Audio data size
    au_file.write(struct.pack('>I', encoding))             # Encoding format
    au_file.write(struct.pack('>I', sample_rate))          # Sample rate
    au_file.write(struct.pack('>I', channels))             # Number of channels
    
    # Write the audio data
    for sample in audio_data:
        au_file.write(struct.pack('>h', sample))

print(f"AU file generated and saved to {output_file}")