import customtkinter as ctk
import os
from tkinter import filedialog

class ThockifyApp(ctk.CTk):
    def __init__(self, config, sound_engine):
        super().__init__()

        self.config = config
        self.sound_engine = sound_engine

        self.title("Thockify")
        self.geometry("400x600")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self._init_ui()

    def _init_ui(self):
        # Main Container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.label_title = ctk.CTkLabel(self.main_frame, text="Thockify", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=(10, 20))

        # --- Sound Settings Frame ---
        self.frame_sound = ctk.CTkFrame(self.main_frame)
        self.frame_sound.pack(fill="x", pady=10)

        # Sound Pack Selector
        self.label_pack = ctk.CTkLabel(self.frame_sound, text="Sound Pack")
        self.label_pack.pack(pady=(10, 0))
        
        self.packs = self._get_available_packs()
        self.pack_var = ctk.StringVar(value=self.config.get("sound_pack"))
        self.option_pack = ctk.CTkOptionMenu(self.frame_sound, values=self.packs, variable=self.pack_var, command=self.change_pack)
        self.option_pack.pack(pady=5)

        # Custom Folder Button
        self.btn_custom = ctk.CTkButton(self.frame_sound, text="Open Custom Folder", command=self.open_custom_folder, height=24, fg_color="transparent", border_width=1)
        self.btn_custom.pack(pady=(5, 10))

        # --- Audio Controls Frame ---
        self.frame_audio = ctk.CTkFrame(self.main_frame)
        self.frame_audio.pack(fill="x", pady=10)

        # Volume Control
        self.label_volume = ctk.CTkLabel(self.frame_audio, text="Volume")
        self.label_volume.pack(pady=(10, 0))
        
        self.slider_volume = ctk.CTkSlider(self.frame_audio, from_=0, to=1, command=self.change_volume)
        self.slider_volume.set(self.config.get("volume"))
        self.slider_volume.pack(pady=5)

        # Pitch Variation Control
        self.label_pitch = ctk.CTkLabel(self.frame_audio, text="Pitch Randomness")
        self.label_pitch.pack(pady=(10, 0))

        self.slider_pitch = ctk.CTkSlider(self.frame_audio, from_=0, to=0.2, command=self.change_pitch)
        self.slider_pitch.set(self.config.get("pitch_variation"))
        self.slider_pitch.pack(pady=5)

        # --- Settings Frame ---
        self.frame_settings = ctk.CTkFrame(self.main_frame)
        self.frame_settings.pack(fill="x", pady=10)

        # Start Minimized Checkbox
        self.var_minimized = ctk.BooleanVar(value=self.config.get("start_minimized"))
        self.chk_minimized = ctk.CTkCheckBox(self.frame_settings, text="Start Minimized", variable=self.var_minimized, command=self.toggle_minimized)
        self.chk_minimized.pack(pady=10)

        # Status
        self.label_status = ctk.CTkLabel(self.main_frame, text="Status: Running", text_color="green")
        self.label_status.pack(pady=10, side="bottom")

    def change_pitch(self, value):
        self.config.set("pitch_variation", value)

    def toggle_minimized(self):
        self.config.set("start_minimized", self.var_minimized.get())

    def _get_available_packs(self):
        assets_dir = os.path.join(os.getcwd(), "assets")
        if not os.path.exists(assets_dir):
            return ["Default"]
        return [d for d in os.listdir(assets_dir) if os.path.isdir(os.path.join(assets_dir, d))]

    def change_pack(self, choice):
        print(f"Changing pack to: {choice}")
        self.config.set("sound_pack", choice)
        self.sound_engine.load_pack(choice)

    def change_volume(self, value):
        self.sound_engine.update_volume(value)

    def open_custom_folder(self):
        # Open the assets folder in file explorer
        path = os.path.join(os.getcwd(), "assets")
        if os.name == 'nt':
            os.startfile(path)
        else:
            # Linux/Unix
            os.system(f"xdg-open '{path}'")
