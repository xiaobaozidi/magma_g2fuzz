import numpy as np
from scipy.io.wavfile import write
import os

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters
sample_rate = 44100  # Sampling rate in Hz
duration = 2  # Duration in seconds

# Generate a time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a sample tone (440Hz sine wave)
frequency = 440  # Frequency of the tone in Hz
tone = 0.5 * np.sin(2 * np.pi * frequency * t)

# Mono configuration
mono_data = tone
write(os.path.join(output_dir, 'mono.wav'), sample_rate, mono_data.astype(np.float32))

# Stereo configuration
stereo_data = np.column_stack((tone, tone))  # Duplicate the tone for both channels
write(os.path.join(output_dir, 'stereo.wav'), sample_rate, stereo_data.astype(np.float32))

# Multi-channel (5.1 surround sound) configuration
# 5.1 channels: Front Left, Front Right, Center, LFE (Low-Frequency Effects), Rear Left, Rear Right
# For simplicity, the same tone is used for all channels, but you could use different signals for realism
channels_5_1 = np.column_stack((tone, tone, tone, tone, tone, tone))
write(os.path.join(output_dir, 'multichannel_5_1.wav'), sample_rate, channels_5_1.astype(np.float32))