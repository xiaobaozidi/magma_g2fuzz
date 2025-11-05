import numpy as np
import wave
import os

# Create the directory to save the wav files if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Function to generate and save a sine wave with a given sample rate
def generate_sine_wave(frequency, sample_rate, duration, filename):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    waveform_integers = np.int16(waveform * 32767)
    
    with wave.open(filename, 'w') as wav_file:
        # Set the parameters for the WAV file
        n_channels = 1
        sampwidth = 2  # 2 bytes per sample
        n_frames = len(waveform_integers)
        comptype = "NONE"
        compname = "not compressed"
        
        wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, comptype, compname))
        wav_file.writeframes(waveform_integers.tobytes())

# Parameters for WAV files
frequencies = [440]  # A4 note frequency in Hz
duration = 2.0  # 2 seconds duration

# Sample rates to generate
sample_rates = [44100, 48000]

# Generate and save WAV files
for sample_rate in sample_rates:
    filename = os.path.join(output_dir, f"sine_wave_{sample_rate}Hz.wav")
    generate_sine_wave(frequencies[0], sample_rate, duration, filename)