import numpy as np
from scipy.io.wavfile import write
import os

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the sine wave
samplerate = 44100  # Sample rate in Hz
duration = 2        # Duration in seconds
frequency = 440.0   # Frequency of the sine wave in Hz (A4 note)

# Generate the time axis
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)

# Generate the sine wave
amplitude = 0.5 * np.iinfo(np.int16).max  # Max amplitude for int16
audio_data = amplitude * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM format
audio_data = audio_data.astype(np.int16)

# Define the output file path
output_file = os.path.join(output_dir, 'sine_wave.wav')

# Write the WAV file
write(output_file, samplerate, audio_data)

print(f"WAV file saved as {output_file}")