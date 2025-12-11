from pynput import keyboard
import threading

class InputListener:
    def __init__(self, sound_engine):
        self.sound_engine = sound_engine
        self.listener = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.pressed_keys = set()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Input listener started.")

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.running = False

    def on_press(self, key):
        if key in self.pressed_keys:
            return
        
        self.pressed_keys.add(key)
        
        try:
            key_type = "base"
            
            if key == keyboard.Key.space:
                key_type = "space"
            elif key == keyboard.Key.enter:
                key_type = "enter"
            elif key == keyboard.Key.backspace:
                key_type = "backspace"
            # Add more mappings here
            
            self.sound_engine.play(key_type)
            
        except Exception as e:
            print(f"Error in listener: {e}")

    def on_release(self, key):
        try:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except KeyError:
            pass
