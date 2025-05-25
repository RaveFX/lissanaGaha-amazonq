import numpy as np
import wave
import struct
import os

def create_sine_wave(frequency, duration_ms, volume=0.5, sample_rate=44100):
    """
    Create a sine wave with the given frequency and duration
    
    Args:
        frequency: Frequency in Hz
        duration_ms: Duration in milliseconds
        volume: Volume between 0 and 1
        sample_rate: Sample rate in Hz
    
    Returns:
        Numpy array of audio samples
    """
    num_samples = int(duration_ms * sample_rate / 1000)
    t = np.linspace(0, duration_ms / 1000, num_samples, endpoint=False)
    wave_data = np.sin(2 * np.pi * frequency * t) * volume
    return wave_data

def create_climb_sound():
    """Create a short climbing sound effect"""
    sample_rate = 44100
    audio = create_sine_wave(440, 50, 0.3, sample_rate)
    audio += create_sine_wave(550, 50, 0.2, sample_rate)
    # Apply envelope
    envelope = np.linspace(0.5, 1.0, len(audio))
    audio = audio * envelope
    return audio, sample_rate

def create_slip_sound():
    """Create a slipping sound effect"""
    sample_rate = 44100
    duration = 300
    audio = np.zeros(int(duration * sample_rate / 1000))
    
    # Create a downward sweep
    for i in range(100):
        freq = 800 - i * 5
        start = int(i * sample_rate / 1000)
        end = int((i + 3) * sample_rate / 1000)
        if end > len(audio):
            end = len(audio)
        t = np.linspace(0, 3/1000, end-start, endpoint=False)
        audio[start:end] += np.sin(2 * np.pi * freq * t) * 0.4
    
    # Apply envelope
    envelope = np.linspace(1.0, 0.1, len(audio))
    audio = audio * envelope
    return audio, sample_rate

def create_hit_sound():
    """Create a coconut hit sound effect"""
    sample_rate = 44100
    duration = 200
    audio = np.zeros(int(duration * sample_rate / 1000))
    
    # Create a thud sound
    audio += create_sine_wave(150, duration, 0.7, sample_rate)
    audio += create_sine_wave(80, duration, 0.5, sample_rate)
    
    # Add some noise
    noise = np.random.uniform(-0.2, 0.2, len(audio))
    audio = audio + noise
    
    # Apply envelope
    envelope = np.exp(-np.linspace(0, 10, len(audio)))
    audio = audio * envelope
    return audio, sample_rate

def save_wave_file(filename, audio_data, sample_rate):
    """Save audio data to a WAV file"""
    # Ensure the audio is normalized between -1 and 1
    audio_data = np.clip(audio_data, -1, 1)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Convert to bytes
        for sample in audio_data:
            wav_file.writeframes(struct.pack('h', sample))
    
    print(f"Created {filename}")

def main():
    # Create the assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Create and save climb sound
    audio, sample_rate = create_climb_sound()
    save_wave_file(os.path.join(assets_dir, 'climb.wav'), audio, sample_rate)
    
    # Create and save slip sound
    audio, sample_rate = create_slip_sound()
    save_wave_file(os.path.join(assets_dir, 'slip.wav'), audio, sample_rate)
    
    # Create and save hit sound
    audio, sample_rate = create_hit_sound()
    save_wave_file(os.path.join(assets_dir, 'hit.wav'), audio, sample_rate)
    
    print("All missing sound files have been created!")

if __name__ == "__main__":
    main()
