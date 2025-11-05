import wave
import os
import numpy as np

# Directory to save the generated AIFF file
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Filename for the AIFF file
filename = 'extensible_format.aiff'
file_path = os.path.join(output_dir, filename)

# Sample rate and duration
sample_rate = 44100  # Hz
duration = 1  # seconds
n_channels = 1
sample_width = 2  # bytes (16-bit audio)
n_frames = sample_rate * duration

# Generate a simple sine wave signal
frequency = 440.0  # A4 note, 440 Hz
t = np.linspace(0, duration, n_frames, endpoint=False)
audio_data = (0.5 * np.sin(2 * np.pi * frequency * t) * (2**(8*sample_width-1)-1)).astype(np.int16)

# Create the AIFF file with a custom chunk for extensibility
with wave.open(file_path, 'w') as wave_file:
    wave_file.setnchannels(n_channels)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(sample_rate)
    wave_file.setnframes(n_frames)

    # Write audio data
    wave_file.writeframes(audio_data.tobytes())

    # Add a custom chunk (Note: wave module does not support custom chunks directly)
    # Custom chunks are not supported by the wave module, so this part is omitted.

print(f'AIFF file created at: {file_path}')