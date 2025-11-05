import numpy as np
from scipy.io import wavfile
import os

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define parameters for the audio signal
duration = 2  # seconds
frequency = 440.0  # A4 note, 440 Hz

# List of sample rates to generate files for
sample_rates = [8000, 16000, 44100]

# Function to generate a sine wave
def generate_sine_wave(frequency, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio_data

# Generate and save .au files for each sample rate
for sample_rate in sample_rates:
    audio_data = generate_sine_wave(frequency, sample_rate, duration)
    # Normalize to 16-bit PCM range
    audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
    # Save as .au file
    au_file_path = os.path.join(output_dir, f'sine_wave_{sample_rate}.au')
    wavfile.write(au_file_path, sample_rate, audio_data)

print("AU files generated successfully in the ./tmp/ directory.")