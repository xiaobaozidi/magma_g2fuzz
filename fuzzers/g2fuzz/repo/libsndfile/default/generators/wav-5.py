import wave
import os
import struct
import math  # Import the math module

# Create a directory for saving the WAV file if it doesn't exist
os.makedirs('./tmp', exist_ok=True)

# Parameters for the WAV file
n_channels = 1  # mono
sampwidth = 2   # 2 bytes per sample
framerate = 44100  # 44.1 kHz
n_frames = framerate * 1  # 1 second of audio
comptype = 'NONE'
compname = 'not compressed'

# Generate a simple waveform (e.g., a sine wave)
frequency = 440.0  # Frequency in Hz (A4 note)
amplitude = 32767  # Max amplitude for 16-bit audio

# Create a WAV file with metadata
filename = './tmp/sine_wave_with_metadata.wav'
with wave.open(filename, 'w') as wav_file:
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(sampwidth)
    wav_file.setframerate(framerate)
    wav_file.setcomptype(comptype, compname)

    # Generate the audio samples
    for i in range(n_frames):
        sample_value = int(amplitude * 0.5 * (1.0 + math.sin(2.0 * math.pi * frequency * i / framerate)))
        sample = struct.pack('<h', sample_value)
        wav_file.writeframes(sample)

    # Add metadata
    # The 'LIST' chunk is used to store metadata in WAV files
    metadata = (
        b'LIST' +
        struct.pack('<I', 4 + 4 + 4 + 4 + len('ARTIST') + 1 + 4 + 4 + len('Python') + 1) +
        b'INFO' +
        b'IART' +
        struct.pack('<I', len('Python') + 1) + b'Python' + b'\0' +
        b'INAM' +
        struct.pack('<I', len('Sine Wave') + 1) + b'Sine Wave' + b'\0'
    )
    wav_file._file.write(metadata)

print(f"WAV file with metadata saved to {filename}")