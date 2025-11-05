import numpy as np
import scipy.io.wavfile as wav
import os

# Create a directory to save the generated files if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the WAV file
sample_rate = 44100  # Standard CD-quality sample rate
duration = 2  # 2 seconds
frequency = 440  # Frequency of the generated tone (A4 note)

# Generate a sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = np.sin(2 * np.pi * frequency * t)

# Save WAV files with different bit depths
bit_depths = [8, 16, 24, 32]
for bit_depth in bit_depths:
    if bit_depth == 8:
        # 8-bit audio is typically unsigned
        audio_scaled = np.int8((audio_data + 1) * 127.5)
    elif bit_depth == 16:
        audio_scaled = np.int16(audio_data * 32767)
    elif bit_depth == 24:
        # 24-bit audio needs special handling
        max_amplitude = 2**23 - 1
        audio_scaled = np.int32(audio_data * max_amplitude)
        # Convert to bytes and write manually
        audio_bytes = audio_scaled.astype(np.int32).tobytes()
        file_name = f'{output_dir}sine_wave_{bit_depth}bit.wav'
        with open(file_name, 'wb') as f:
            # Write WAV header manually
            f.write(b'RIFF')
            f.write((36 + len(audio_bytes)).to_bytes(4, 'little'))
            f.write(b'WAVE')
            f.write(b'fmt ')
            f.write((16).to_bytes(4, 'little'))  # Subchunk1Size (16 for PCM)
            f.write((1).to_bytes(2, 'little'))   # AudioFormat (1 for PCM)
            f.write((1).to_bytes(2, 'little'))   # NumChannels
            f.write(sample_rate.to_bytes(4, 'little'))
            byte_rate = sample_rate * 3  # 3 bytes per sample
            f.write(byte_rate.to_bytes(4, 'little'))
            block_align = 3  # 3 bytes per sample
            f.write(block_align.to_bytes(2, 'little'))
            f.write((24).to_bytes(2, 'little'))  # BitsPerSample
            f.write(b'data')
            f.write(len(audio_bytes).to_bytes(4, 'little'))
            f.write(audio_bytes)
        continue  # Skip the default writing process for 24-bit
    elif bit_depth == 32:
        audio_scaled = np.int32(audio_data * 2147483647)
    
    file_name = f'{output_dir}sine_wave_{bit_depth}bit.wav'
    wav.write(file_name, sample_rate, audio_scaled)