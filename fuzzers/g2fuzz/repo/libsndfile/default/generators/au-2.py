import numpy as np
from scipy.io import wavfile
import os

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define parameters for the audio file
sample_rate = 8000  # 8 kHz sample rate
duration_seconds = 2  # 2 seconds of audio
frequency = 440.0  # A4 note, 440 Hz

# Generate a time array
t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds), endpoint=False)

# Generate a sine wave (A4 note)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

# Convert to μ-law encoding
mu_law_encoded = np.sign(audio_data) * np.log1p(255 * np.abs(audio_data)) / np.log1p(255)

# Scale to 16-bit PCM range
pcm_encoded = np.int16(audio_data * 32767)

# Save the μ-law encoded audio as AU file
mu_law_file_path = os.path.join(output_dir, 'mu_law.au')
with open(mu_law_file_path, 'wb') as f:
    # Write a simple AU header
    f.write(b'.snd')
    f.write((24).to_bytes(4, byteorder='big'))  # Data offset
    f.write((len(mu_law_encoded)).to_bytes(4, byteorder='big'))  # Data size
    f.write((1).to_bytes(4, byteorder='big'))  # Encoding μ-law
    f.write((sample_rate).to_bytes(4, byteorder='big'))  # Sample rate
    f.write((1).to_bytes(4, byteorder='big'))  # Channels
    # Write the audio data
    mu_law_encoded_bytes = ((mu_law_encoded + 1) * 127.5).astype(np.uint8)
    f.write(mu_law_encoded_bytes.tobytes())

# Save the PCM encoded audio as AU file
pcm_file_path = os.path.join(output_dir, 'pcm.au')
with open(pcm_file_path, 'wb') as f:
    # Write a simple AU header
    f.write(b'.snd')
    f.write((24).to_bytes(4, byteorder='big'))  # Data offset
    f.write((len(pcm_encoded) * 2).to_bytes(4, byteorder='big'))  # Data size
    f.write((3).to_bytes(4, byteorder='big'))  # Encoding PCM
    f.write((sample_rate).to_bytes(4, byteorder='big'))  # Sample rate
    f.write((1).to_bytes(4, byteorder='big'))  # Channels
    # Write the audio data
    f.write(pcm_encoded.tobytes())

print(f"Generated μ-law encoded AU file: {mu_law_file_path}")
print(f"Generated PCM encoded AU file: {pcm_file_path}")