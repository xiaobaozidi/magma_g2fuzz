import os
import wave
import struct
import math

# Create the output directory if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Define a simple sine wave function for generating audio data
def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=32767):
    num_samples = int(sample_rate * duration)
    samples = [
        amplitude * 0.5 * (1 + math.sin(2 * math.pi * frequency * x / sample_rate))
        for x in range(num_samples)
    ]
    return samples

# Generate a simple wav file with extensibility chunks
def generate_wave_with_extensibility(filename, frequency=440, duration=2):
    sample_rate = 44100
    amplitude = 32767
    samples = generate_sine_wave(frequency, duration, sample_rate, amplitude)

    # Save wave file
    with wave.open(filename, 'wb') as wav_file:
        n_channels = 1
        sampwidth = 2  # 2 bytes per sample
        wav_file.setparams((n_channels, sampwidth, sample_rate, len(samples), 'NONE', 'not compressed'))

        # Write samples
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', int(sample)))

        # Add custom extensibility chunk
        # Format for a chunk: 4 bytes for chunk id, 4 bytes for chunk size, then the chunk data
        extensibility_chunk_id = b'extn'
        extensibility_chunk_data = b'Custom extensibility data for demonstration.'
        chunk_size = len(extensibility_chunk_data)
        
        wav_file.writeframes(extensibility_chunk_id)
        wav_file.writeframes(struct.pack('<I', chunk_size))
        wav_file.writeframes(extensibility_chunk_data)

# Generate the file
generate_wave_with_extensibility(os.path.join(output_dir, 'extensible_wave.wav'))