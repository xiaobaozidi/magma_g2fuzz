import wave
import struct
import os
import math  # Import the math module for mathematical functions

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define basic properties for the audio
sample_rate = 44100  # Samples per second
duration = 2         # Duration in seconds
frequency = 440.0    # Frequency of the sine wave (A4 note)

# Generate sine wave data
num_samples = int(sample_rate * duration)
amplitude = 32767  # Max amplitude for 16-bit audio
audio_data = []

for n in range(num_samples):
    # Use math.sin instead of struct.sin
    sample = amplitude * (0.5 * (1.0 + math.sin(2 * 3.141592653589793 * frequency * n / sample_rate)))
    audio_data.append(int(sample))

# Convert audio data to bytes
audio_bytes = struct.pack('<' + ('h' * len(audio_data)), *audio_data)

# Define BWF metadata (example)
bext_chunk_data = (
    b'example description\0' * 64 +         # Description
    b'example originator\0' * 32 +          # Originator
    b'example originator ref\0' * 32 +      # Originator Reference
    b'2023-10-01T12:34:56\0' * 10 +         # Origination Date
    b'12:34:56\0' * 8 +                     # Origination Time
    struct.pack('<Q', num_samples) +        # Time Reference (sample count)
    b'example umid\0' * 64 +                # UMID
    struct.pack('<h', 0)                    # Reserved
)

# Create the WAV file with BWF (Broadcast Wave Format) support
with wave.open(os.path.join(output_dir, 'bwf_example.wav'), 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 16-bit audio
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_bytes)

    # Write BEXT chunk for BWF
    wav_file._file.write(b'bext')
    wav_file._file.write(struct.pack('<I', len(bext_chunk_data)))  # Chunk size
    wav_file._file.write(bext_chunk_data)