import os
from scipy.io import wavfile
import numpy as np
import sunau

# Create the output directory if it doesn't exist
output_dir = './tmp/'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the audio file
sample_rate = 8000  # 8kHz sample rate
duration = 5  # 5 seconds duration
frequency = 440  # A4 note frequency in Hz (standard musical pitch)

# Generate a sine wave as a simple audio signal
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = (0.5 * np.sin(2 * np.pi * frequency * t)).astype(np.float32)

# Save the audio data as an 'au' file
output_file_path = os.path.join(output_dir, 'example.au')

# Use sunau to write the AU file
with sunau.open(output_file_path, 'w') as au_file:
    au_file.setnchannels(1)  # mono audio
    au_file.setsampwidth(2)  # 16-bit samples
    au_file.setframerate(sample_rate)
    
    # Convert float32 data to int16 for saving
    int_data = np.int16(audio_data * 32767)  # Scale to int16 range
    au_file.writeframes(int_data.tobytes())

print(f"AU file generated and saved to {output_file_path}")