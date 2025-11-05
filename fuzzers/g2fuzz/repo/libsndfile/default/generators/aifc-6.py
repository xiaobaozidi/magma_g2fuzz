import wave
import os
import numpy as np

# Create the directory if it doesn't exist
os.makedirs('./tmp/', exist_ok=True)

# Parameters for the audio file
sample_rate = 44100  # CD quality
duration_seconds = 2  # 2 seconds of audio
frequency = 440.0  # A4 note, standard pitch (440 Hz)
num_channels = 1  # Mono audio
sample_width = 2  # 2 bytes per sample (16 bits)

# Generate a sine wave
t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds), endpoint=False)
audio_data = (0.5 * np.sin(2 * np.pi * frequency * t) * (2**15 - 1)).astype(np.int16)

# File path
file_path = './tmp/generated_audio.aiff'

# Write the data to an AIFF file
with wave.open(file_path, 'w') as wave_file:
    wave_file.setnchannels(num_channels)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(sample_rate)
    
    # Prepare the data in bytes
    byte_data = audio_data.tobytes()
    
    # Write the byte data to the file
    wave_file.writeframes(byte_data)

print(f"AIFF file generated at: {file_path}")