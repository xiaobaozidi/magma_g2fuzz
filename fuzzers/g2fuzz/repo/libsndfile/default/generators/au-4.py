import os
import numpy as np
from scipy.io import wavfile

def generate_au_file(filename, samplerate, data):
    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the data as a WAV file (intermediate step)
    wav_filename = filename.replace('.au', '.wav')
    wavfile.write(wav_filename, samplerate, data)
    
    # Convert WAV to AU using an external tool like ffmpeg
    os.system(f"ffmpeg -y -i {wav_filename} -c:a pcm_s16be {filename}")

# Parameters
samplerate = 44100  # Sample rate in Hz

# Generate mono audio data (single channel)
duration = 2  # seconds
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
mono_data = 0.5 * np.sin(2 * np.pi * 440 * t)  # A simple sine wave at 440 Hz

# Generate stereo audio data (two channels)
stereo_data = np.column_stack((mono_data, mono_data))  # Just duplicate the mono data

# Convert data to the right format (16-bit PCM)
mono_data_pcm = (mono_data * 32767).astype(np.int16)
stereo_data_pcm = (stereo_data * 32767).astype(np.int16)

# File paths
mono_au_file = './tmp/mono.au'
stereo_au_file = './tmp/stereo.au'

# Generate AU files
generate_au_file(mono_au_file, samplerate, mono_data_pcm)
generate_au_file(stereo_au_file, samplerate, stereo_data_pcm)