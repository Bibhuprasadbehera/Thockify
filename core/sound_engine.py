import os
import random
import pygame

class SoundEngine:
    def __init__(self, config_manager):
        self.config = config_manager
        # Pre-init mixer with smaller buffer for lower latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)  # Allow multiple sounds at once
        self.sounds = {}
        self.current_pack_path = ""
        self.load_pack(self.config.get("sound_pack"))

    def load_pack(self, pack_name):
        # Determine path (handle built-in vs custom later)
        # For now assuming all are in assets/
        base_path = os.path.join(os.getcwd(), "assets", pack_name)
        if not os.path.exists(base_path):
            print(f"Sound pack not found: {base_path}")
            return

        self.current_pack_path = base_path
        self.sounds = {}
        
        # Load standard keys
        self._load_sound(base_path, "base", "base.wav")
        self._load_sound(base_path, "space", "space.wav")
        self._load_sound(base_path, "enter", "enter.wav")
        self._load_sound(base_path, "backspace", "backspace.wav")
        # Add more specials as needed

        print(f"Loaded sound pack: {pack_name}")

    def _load_sound(self, base_path, key, filename):
        path = os.path.join(base_path, filename)
        if os.path.exists(path):
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
                self.sounds[key].set_volume(self.config.get("volume"))
            except Exception as e:
                print(f"Failed to load sound {path}: {e}")
        else:
            # Fallback to base if special missing
            if key != "base" and "base" in self.sounds:
                self.sounds[key] = self.sounds["base"]

    def play(self, key_type="base"):
        sound = self.sounds.get(key_type, self.sounds.get("base"))
        if sound:
            # Pitch variation is tricky with standard pygame mixer without numpy/resampling
            # For now, just play. We can add volume variation.
            
            vol = self.config.get("volume")
            # Slight volume variation
            if self.config.get("pitch_variation") > 0:
                 variation = random.uniform(-0.05, 0.05)
                 sound.set_volume(max(0.0, min(1.0, vol + variation)))
            else:
                sound.set_volume(vol)
                
            sound.play()

    def update_volume(self, volume):
        self.config.set("volume", volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)
