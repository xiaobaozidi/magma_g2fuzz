import numpy as np
import wave
import aifc
import os

# Create the output directory if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the AIFF file
sample_rate = 44100  # Standard CD-quality sample rate
duration = 2  # 2 seconds
frequency = 440  # A4 note frequency in Hz

# Generate a PCM waveform (sine wave)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Normalize audio_data to 16-bit PCM format
audio_data = np.int16(audio_data * 32767)

# Save the AIFF file
file_path = os.path.join(output_dir, 'sine_wave.aiff')
with aifc.open(file_path, 'w') as aiff_file:
    aiff_file.setnchannels(1)  # Mono
    aiff_file.setsampwidth(2)  # 16 bits per sample
    aiff_file.setframerate(sample_rate)
    aiff_file.writeframes(audio_data.tobytes())

print(f"AIFF file saved to {file_path}")