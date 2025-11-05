import os
import struct
import numpy as np
from scipy.io import wavfile

def create_au_file(file_path, sample_rate, audio_data, comment=""):
    # Define AU header constants
    AU_HEADER_SIZE = 24
    AU_MAGIC = b'.snd'
    AU_ENCODING = 2  # 16-bit linear PCM
    AU_HEADER_LENGTH = AU_HEADER_SIZE + len(comment.encode('utf-8')) + 1  # +1 for null-terminated comment

    # Calculate the data size
    if audio_data.dtype != np.int16:
        raise ValueError("Audio data must be in 16-bit PCM format.")
    data_size = audio_data.nbytes

    # Prepare AU header
    header = struct.pack(
        '>4s5L',  # Big-endian: magic, header size, data size, encoding, sample rate, channels
        AU_MAGIC,
        AU_HEADER_LENGTH,
        data_size,
        AU_ENCODING,
        sample_rate,
        1  # Mono audio
    )

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the AU file
    with open(file_path, 'wb') as f:
        f.write(header)
        f.write(comment.encode('utf-8') + b'\x00')  # Null-terminated comment
        f.write(audio_data.tobytes())

# Generate a simple sine wave as audio data
def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    return np.int16(audio_data * 32767)

# Parameters
sample_rate = 8000  # 8 kHz
frequency = 440  # A4
duration = 2  # 2 seconds
comment = "Generated AU file with basic metadata."

# Generate audio data
audio_data = generate_sine_wave(frequency, duration, sample_rate)

# Create AU file
file_path = './tmp/test.au'
create_au_file(file_path, sample_rate, audio_data, comment)