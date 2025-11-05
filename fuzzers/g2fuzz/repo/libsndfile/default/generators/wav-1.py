import numpy as np
import wave
import os

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the audio file
sample_rate = 44100  # Samples per second
duration = 2  # Duration in seconds
frequency = 440.0  # Frequency of the sine wave (A4 note)

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to 16-bit PCM format
audio_data = (audio_data * 32767).astype(np.int16)

# Path to save the WAV file
file_path = os.path.join(output_dir, 'sine_wave.wav')

# Write the WAV file
with wave.open(file_path, 'w') as wf:
    wf.setnchannels(1)  # Mono audio
    wf.setsampwidth(2)  # 2 bytes per sample (16 bits)
    wf.setframerate(sample_rate)
    wf.writeframes(audio_data.tobytes())

print(f"WAV file generated and saved to {file_path}")