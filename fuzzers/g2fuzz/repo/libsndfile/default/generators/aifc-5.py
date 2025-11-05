import os
import aifc
from mutagen import aiff
from mutagen.id3 import ID3, TIT2, TPE1, TALB

# Create the output directory if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# File path for the new AIFC file
file_path = os.path.join(output_dir, 'example.aifc')

# Generate a simple sine wave as audio data
import numpy as np

# Parameters for the audio
sample_rate = 44100  # 44.1 kHz
duration_seconds = 2
frequency = 440.0  # A4 note, 440 Hz
num_frames = int(sample_rate * duration_seconds)
time_points = np.linspace(0, duration_seconds, num_frames, endpoint=False)

# Generate audio data
audio_data = (0.5 * np.sin(2 * np.pi * frequency * time_points)).astype(np.float32)

# Write audio data to an AIFC file
with aifc.open(file_path, 'w') as aifc_file:
    # Set parameters: 1 channel, 4 bytes per sample, sample rate, and number of frames
    aifc_file.setnchannels(1)
    aifc_file.setsampwidth(4)
    aifc_file.setframerate(sample_rate)
    aifc_file.setnframes(num_frames)

    # Write audio data
    aifc_file.writeframes(audio_data.tobytes())

# Add metadata using mutagen
aiff_file = aiff.AIFF(file_path)

# Create an ID3 tag if it doesn't exist
if not aiff_file.tags:
    aiff_file.add_tags()

# Set metadata
aiff_file.tags.add(TIT2(encoding=3, text='Example Track'))
aiff_file.tags.add(TPE1(encoding=3, text='Example Artist'))
aiff_file.tags.add(TALB(encoding=3, text='Example Album'))

# Save the changes
aiff_file.save()

print(f"AIFC file with metadata saved to: {file_path}")