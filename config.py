import json
import os

class ConfigManager:
    DEFAULT_CONFIG = {
        "sound_pack": "blue",
        "volume": 0.8,
        "pitch_variation": 0.05,
        "start_minimized": False
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
