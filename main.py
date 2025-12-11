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
    listener = None
    
    # Try evdev on Linux (requires root or input group)
    if sys.platform.startswith("linux"):
        try:
            from core.listener_linux import LinuxInputListener
            # Check permissions by trying to open a device
            import evdev
            try:
                devices = evdev.list_devices()
                if not devices:
                    raise PermissionError("No devices found (empty list).")
                # Try opening the first device to verify read permissions
                evdev.InputDevice(devices[0])
                
                print("Permissions ok for evdev. Using LinuxInputListener.")
                listener = LinuxInputListener(sound_engine)
            except (PermissionError, OSError):
                print("Permission denied for evdev (device access). Falling back to pynput.")
                print("Tip: Run 'sudo ./setup_permissions.sh' then LOG OUT to fix.")
                raise ImportError("Force fallback") # Trigger outer except
        except ImportError:
            pass

    if listener is None:
        from core.listener import InputListener
        print("Using pynput listener (Window-local only).")
        listener = InputListener(sound_engine)

    # Start listener with error handling
    try:
        listener.start()
    except Exception as e:
        print(f"Failed to start listener: {e}")
        sys.exit(1)

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
