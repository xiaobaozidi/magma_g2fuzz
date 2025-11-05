import numpy as np
from scipy.io import wavfile
import os

# Directory to save the WAV file
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# File name
file_name = 'large_file.wav'
file_path = os.path.join(output_dir, file_name)

# Audio properties
sample_rate = 44100  # CD quality sample rate
duration_seconds = 60 * 10  # 10 minutes
channels = 2  # Stereo

# Generate random audio data
# The data will be in the range of int16, which is standard for WAV files
audio_data = np.random.randint(
    -32768, 32767, sample_rate * duration_seconds * channels, dtype=np.int16
)

# Reshape the data to have the correct number of channels
audio_data = audio_data.reshape((-1, channels))

# Save the audio data as a WAV file
wavfile.write(file_path, sample_rate, audio_data)

print(f"WAV file with large size saved to: {file_path}")