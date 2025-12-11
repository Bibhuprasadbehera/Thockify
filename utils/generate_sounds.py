import wave
import math
import struct
import os
import random

def generate_beep(filename, frequency=440, duration=0.1, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Simple sine wave with decay
            t = float(i) / sample_rate
            decay = 1.0 - (float(i) / n_samples)
            value = int(32767.0 * volume * decay * math.sin(2.0 * math.pi * frequency * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

def main():
    packs = {
        "blue": 2000, # High pitch click
        "brown": 800, # Medium bump
        "red": 400    # Low thud
    }
    
    base_dir = os.path.join(os.getcwd(), "assets")
    
    for pack, freq in packs.items():
        pack_dir = os.path.join(base_dir, pack)
        if not os.path.exists(pack_dir):
            os.makedirs(pack_dir)
            
        print(f"Generating sounds for {pack}...")
        
        # Base key
        generate_beep(os.path.join(pack_dir, "base.wav"), freq, 0.1)
        
        # Space (lower pitch, longer)
        generate_beep(os.path.join(pack_dir, "space.wav"), freq * 0.8, 0.15)
        
        # Enter (slightly different)
        generate_beep(os.path.join(pack_dir, "enter.wav"), freq * 0.9, 0.12)
        
        # Backspace (higher pitch)
        generate_beep(os.path.join(pack_dir, "backspace.wav"), freq * 1.2, 0.1)

if __name__ == "__main__":
    main()
