import evdev
import select
import threading
import time

class LinuxInputListener:
    def __init__(self, sound_engine):
        self.sound_engine = sound_engine
        self.running = False
        self.thread = None
        self.devices = []
        self.REPEAT_DELAY = 0.05 # Ignore repeats faster than this
        self.last_press_time = {}

    def _find_keyboards(self):
        try:
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            keyboards = []
            for dev in devices:
                # Check for EV_KEY capability
                if evdev.ecodes.EV_KEY in dev.capabilities():
                    # Heuristic: Must have KEY_A, KEY_Enter, or KEY_Space
                    keys = dev.capabilities()[evdev.ecodes.EV_KEY]
                    if (evdev.ecodes.KEY_A in keys or 
                        evdev.ecodes.KEY_ENTER in keys or 
                        evdev.ecodes.KEY_SPACE in keys):
                        # Avoid mice or other devices that might declare keys but aren't keyboards
                        # Usually keyboards have many keys.
                        if len(keys) > 10:
                            print(f"Found keyboard: {dev.path} ({dev.name})")
                            keyboards.append(dev)
            return keyboards
        except Exception as e:
            print(f"Error finding keyboards: {e}")
            return []

    def start(self):
        if self.running:
            return
        
        self.devices = self._find_keyboards()
        if not self.devices:
            # Propagate error so main can fallback or alert
            raise PermissionError("No permissions or no devices found.")

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"Linux evdev listener started on {len(self.devices)} devices.")

    def stop(self):
        self.running = False
        if self.thread:
            # unblock select? usually timeout handles it
            self.thread.join(timeout=1.0)
        # Close devices
        for dev in self.devices:
            try:
                dev.close()
            except:
                pass

    def _run_loop(self):
        fds = {dev.fd: dev for dev in self.devices}
        
        while self.running:
            try:
                # select w/ timeout allows checking self.running
                r, w, x = select.select(fds, [], [], 0.5)
                
                for fd in r:
                    dev = fds.get(fd)
                    if not dev: continue
                    
                    try:
                        for event in dev.read():
                            if event.type == evdev.ecodes.EV_KEY:
                                self._process_event(event)
                    except OSError:
                        # Device disconnected?
                        del fds[fd]
                        
            except Exception as e:
                pass
                # print(f"Event loop error: {e}")

    def _process_event(self, event):
        # value: 0=up, 1=down, 2=hold
        if event.value == 1: 
            self._handle_key(event.code)
        elif event.value == 2:
            # Repeat handling if desired, currently ignored for "machine gun" fix
            pass

    def _handle_key(self, key_code):
        key_type = "base"
        
        if key_code == evdev.ecodes.KEY_SPACE:
            key_type = "space"
        elif key_code == evdev.ecodes.KEY_ENTER:
            key_type = "enter"
        elif key_code == evdev.ecodes.KEY_BACKSPACE:
            key_type = "backspace"
        elif key_code in [evdev.ecodes.KEY_LEFTSHIFT, evdev.ecodes.KEY_RIGHTSHIFT,
                          evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_RIGHTCTRL,
                          evdev.ecodes.KEY_LEFTALT, evdev.ecodes.KEY_RIGHTALT,
                          evdev.ecodes.KEY_LEFTMETA, evdev.ecodes.KEY_RIGHTMETA]:
            # Optional: Treat modifiers differently or generic
            pass

        self.sound_engine.play(key_type)
