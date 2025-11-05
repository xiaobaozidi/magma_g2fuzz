import wave
import os
import struct
import numpy as np

# Ensure the directory exists
os.makedirs('./tmp', exist_ok=True)

# Output file path
output_file = './tmp/example.wav'

# Parameters for the audio
n_channels = 1
sampwidth = 2
framerate = 44100
n_frames = 44100  # 1 second of audio

# Generate a simple waveform (e.g., a sine wave)
duration = 1.0  # seconds
frequency = 440.0  # Hz
t = np.linspace(0, duration, int(framerate * duration), endpoint=False)
audio_data = (0.5 * np.sin(2 * np.pi * frequency * t)).astype(np.float32)

# Open the WAV file for writing
with wave.open(output_file, 'w') as wave_file:
    wave_file.setnchannels(n_channels)
    wave_file.setsampwidth(sampwidth)
    wave_file.setframerate(framerate)
    wave_file.setnframes(n_frames)

    # Write the audio data to the file
    for sample in audio_data:
        # Convert the sample to the correct format
        packed_sample = struct.pack('<h', int(sample * 32767))
        wave_file.writeframes(packed_sample)

print(f"WAV file created at: {output_file}")