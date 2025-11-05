import wave
import numpy as np
import struct
import os

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def save_wave_with_loop_points(filename, loop_start, loop_end, sample_rate=44100):
    # Create a directory if it doesn't exist
    os.makedirs('./tmp/', exist_ok=True)

    # Parameters
    duration = 5.0  # 5 seconds
    frequency = 440.0  # A4 note
    amplitude = 32767  # Max amplitude for 16-bit audio

    # Generate sine wave
    wave_data = generate_sine_wave(frequency, duration, sample_rate, amplitude)

    # Convert wave data to 16-bit PCM format
    pcm_data = (wave_data * amplitude).astype(np.int16)

    # Create a new wave file
    with wave.open(filename, 'wb') as wav_file:
        # Set parameters
        nchannels = 1
        sampwidth = 2  # 2 bytes for 'h' format
        nframes = len(pcm_data)
        comptype = "NONE"
        compname = "not compressed"

        wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

        # Write audio data
        wav_file.writeframes(pcm_data.tobytes())

        # Add loop points using 'smpl' chunk
        # smpl chunk structure: https://sites.google.com/site/musicgapi/technical-documents/wav-file-format#smpl
        smpl_chunk_data = b'smpl'  # Chunk ID
        smpl_chunk_data += struct.pack('<I', 60)  # Chunk size
        smpl_chunk_data += struct.pack('<IIIIIIII', 0, 0, 0, 0, 1, 60, 0, 0)  # Basic smpl data
        smpl_chunk_data += struct.pack('<IIIIII', 0, loop_start, loop_end, 0, 0, 0)  # Loop data

        # Write smpl chunk to file
        wav_file._file.write(smpl_chunk_data)

# Define loop points in sample frames
loop_start_frame = 44100  # 1 second
loop_end_frame = 132300   # 3 seconds

# Save the wave file with loop points
save_wave_with_loop_points('./tmp/looped_sine_wave.wav', loop_start_frame, loop_end_frame)