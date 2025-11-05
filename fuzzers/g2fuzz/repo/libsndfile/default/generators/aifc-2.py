import aifc
import os
import numpy as np

# Ensure the ./tmp/ directory exists
os.makedirs('./tmp/', exist_ok=True)

# Parameters for the audio file
n_channels = 2  # Stereo
sample_width = 2  # 2 bytes (16 bits)
framerate = 44100  # Standard CD-quality sample rate
duration_seconds = 5  # Duration of the sound
frequency = 440.0  # Frequency of the tone (A4)

# Calculate the number of frames
n_frames = int(framerate * duration_seconds)

# Generate the audio data
t = np.linspace(0, duration_seconds, n_frames, endpoint=False)
audio_data = (0.5 * 32767 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

# Interleave the channels (same data for left and right channel)
stereo_data = np.column_stack((audio_data, audio_data)).flatten()

# Write the data to an AIFC file
output_file = './tmp/stereo_audio.aifc'
with aifc.open(output_file, 'w') as aifc_file:
    aifc_file.setnchannels(n_channels)
    aifc_file.setsampwidth(sample_width)
    aifc_file.setframerate(framerate)
    aifc_file.writeframes(stereo_data.tobytes())

print(f"Generated AIFC file saved to {output_file}")