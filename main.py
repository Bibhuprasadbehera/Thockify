import sys
import os
import threading
import time
import customtkinter as ctk
from config import ConfigManager
# We will import these later once implemented
# from core.sound_engine import SoundEngine
# from core.listener import InputListener
# from gui.app import ThockifyApp

def main():
    print("Starting Thockify...")
    
    # Initialize Config
    config = ConfigManager()
    print(f"Loaded config: {config.config}")

    # Initialize Sound Engine
    from core.sound_engine import SoundEngine
    sound_engine = SoundEngine(config)

    # Initialize Input Listener
    from core.listener import InputListener
    listener = InputListener(sound_engine)
    listener.start()

    # Initialize GUI
    from gui.app import ThockifyApp
    app = ThockifyApp(config, sound_engine)
    
    # Handle clean exit
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping listener...")
        listener.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
