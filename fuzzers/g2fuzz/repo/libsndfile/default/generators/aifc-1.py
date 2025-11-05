import aifc
import os
import numpy as np

# Ensure the directory exists
os.makedirs('./tmp', exist_ok=True)

# Parameters for the audio
sample_rate = 44100  # Sample rate in Hz
duration = 2  # Duration in seconds
frequency = 440  # Frequency of the sine wave
num_samples = sample_rate * duration

# Generate a sine wave
t = np.linspace(0, duration, num_samples, endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert the float audio data to 16-bit signed integers
audio_data = np.int16(audio_data * 32767)

# Create an AIFC file without explicitly setting a compression type
filename = './tmp/compressed_audio.aifc'
with aifc.open(filename, 'w') as aifc_file:
    # Set the parameters for the AIFC file
    aifc_file.setnchannels(1)  # Mono
    aifc_file.setsampwidth(2)  # 16-bit samples
    aifc_file.setframerate(sample_rate)

    # Write the audio data to the file
    aifc_file.writeframes(audio_data.tobytes())

print(f"AIFC file saved as {filename}")