import os
import numpy as np
import aifc

# Ensure the output directory exists
os.makedirs('./tmp', exist_ok=True)

# Audio parameters
sample_rate = 44100  # 44.1 kHz
duration = 2  # seconds
frequency = 440.0  # A4 note in Hz
bit_depth = 16  # bits
n_channels = 1  # mono

# Calculate the number of samples
n_samples = sample_rate * duration

# Create a sine wave
t = np.linspace(0, duration, int(n_samples), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Scale to 16-bit signed integers
audio_data_int16 = np.int16(audio_data * (2**(bit_depth - 1) - 1))

# Define the file path
file_path = './tmp/high_quality_audio.aifc'

# Write to AIFC file
with aifc.open(file_path, 'w') as aifc_file:
    aifc_file.setnchannels(n_channels)
    aifc_file.setsampwidth(bit_depth // 8)
    aifc_file.setframerate(sample_rate)
    aifc_file.writeframes(audio_data_int16.tobytes())

print(f"AIFC file saved to {file_path}")