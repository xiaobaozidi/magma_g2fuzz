import numpy as np
from scipy.io import wavfile
import os

# Ensure the output directory exists
output_dir = "./tmp/"
os.makedirs(output_dir, exist_ok=True)

# Parameters for the audio file
sample_rate = 44100  # Samples per second
duration = 2  # Duration in seconds
frequency = 440.0  # Frequency of the sine wave (A4 note)

# Generate a time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a sine wave at the given frequency
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Normalize to 16-bit PCM range
audio_data = np.int16(audio_data * 32767)

# Output file path
output_file = os.path.join(output_dir, "sine_wave.aiff")

# Write the audio data to an AIFF file
wavfile.write(output_file, sample_rate, audio_data)