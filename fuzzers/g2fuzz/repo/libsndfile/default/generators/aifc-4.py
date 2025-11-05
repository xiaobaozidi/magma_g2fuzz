import aifc
import os
import numpy as np

# Ensure the output directory exists
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the AIFC file
sample_rate = 44100  # samples per second
duration = 2  # seconds
frequency = 440.0  # A4 note frequency in Hertz
amplitude = 32767  # max amplitude for 16-bit audio

# Generate a simple sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
waveform = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

# Define loop points and markers
loop_start = 0
loop_end = len(waveform) // 2
marker1 = (1, loop_start, b'START_LOOP')  # Marker name as bytes
marker2 = (2, loop_end, b'END_LOOP')      # Marker name as bytes

# File name for the AIFC file
filename = os.path.join(output_dir, 'looping_and_markers.aifc')

# Write the waveform to an AIFC file with markers and loop points
with aifc.open(filename, 'w') as aifc_file:
    aifc_file.setnchannels(1)  # mono audio
    aifc_file.setsampwidth(2)  # 16-bit audio
    aifc_file.setframerate(sample_rate)
    
    # Set markers
    aifc_file.setmark(marker1[0], marker1[1], marker1[2])
    aifc_file.setmark(marker2[0], marker2[1], marker2[2])
    
    # Write audio frames
    aifc_file.writeframes(waveform.tobytes())

print(f"AIFC file with looping and markers saved to {filename}")