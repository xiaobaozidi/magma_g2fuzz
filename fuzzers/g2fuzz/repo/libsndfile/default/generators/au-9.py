import os
import numpy as np
from scipy.io import wavfile

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# AU file header format
def generate_au_header(data_size, sample_rate=8000, channels=1, encoding=1):
    header_size = 24
    header = bytearray(b'.snd')  # Magic number
    header.extend((header_size).to_bytes(4, byteorder='big'))
    header.extend((data_size).to_bytes(4, byteorder='big'))
    header.extend((encoding).to_bytes(4, byteorder='big'))
    header.extend((sample_rate).to_bytes(4, byteorder='big'))
    header.extend((channels).to_bytes(4, byteorder='big'))
    return header

# Generate a simple sine wave signal
def generate_sine_wave(freq, duration, sample_rate=8000, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    return signal

# Create AU file with sine wave
def create_au_file(filename, freq, duration, sample_rate=8000):
    # Generate the sine wave data
    signal = generate_sine_wave(freq, duration, sample_rate)
    
    # Normalize to 16-bit PCM
    max_amplitude = np.iinfo(np.int16).max
    signal = (signal * max_amplitude).astype(np.int16)
    
    # Create AU header
    data_size = len(signal) * 2  # 2 bytes per sample
    header = generate_au_header(data_size, sample_rate)
    
    # Write the header and data to the AU file
    with open(filename, 'wb') as file:
        file.write(header)
        file.write(signal.tobytes())

# Parameters
frequency = 440  # Frequency of the sine wave (A4)
duration = 2     # Duration in seconds

# Generate and save the AU file
au_filename = os.path.join(output_dir, 'sine_wave.au')
create_au_file(au_filename, frequency, duration)

print(f"AU file created at {au_filename}")