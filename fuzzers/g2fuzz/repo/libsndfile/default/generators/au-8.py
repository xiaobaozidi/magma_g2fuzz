import os
import sunau
import numpy as np

def generate_au_file(filename, duration_s, sample_rate, frequency):
    n_samples = int(duration_s * sample_rate)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Open the AU file
    with sunau.open(filename, 'w') as au_file:
        au_file.setnchannels(1)  # Mono
        au_file.setsampwidth(2)  # 16 bits
        au_file.setframerate(sample_rate)
        au_file.setnframes(n_samples)
        
        # Convert audio samples to 16-bit PCM
        pcm_data = (audio_data * (2**15 - 1)).astype(np.int16).tobytes()
        
        # Write the audio data
        au_file.writeframes(pcm_data)

# Parameters for the AU file
filename = './tmp/example.au'
duration_s = 2.0  # 2 seconds
sample_rate = 44100  # 44.1 kHz
frequency = 440.0  # A4 note frequency (440 Hz)

generate_au_file(filename, duration_s, sample_rate, frequency)