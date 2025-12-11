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
        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Container with gradient-like or separate look
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self.frame_header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.label_title = ctk.CTkLabel(self.frame_header, text="THOCKIFY", font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"))
        self.label_title.pack(side="left")
        
        self.label_version = ctk.CTkLabel(self.frame_header, text="v1.0", font=ctk.CTkFont(family="Helvetica", size=12), text_color="gray")
        self.label_version.pack(side="left", padx=10, pady=(12, 0))

        # --- Card: Sound Selection ---
        self.frame_sound = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color=("gray85", "gray20"))
        self.frame_sound.grid(row=1, column=0, sticky="ew", pady=10)
        self.frame_sound.grid_columnconfigure(1, weight=1)

        # Icon/Label
        self.lbl_sound_icon = ctk.CTkLabel(self.frame_sound, text="🎹", font=("Arial", 24))
        self.lbl_sound_icon.grid(row=0, column=0, rowspan=2, padx=15, pady=15)

        self.label_pack = ctk.CTkLabel(self.frame_sound, text="Sound Profile", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_pack.grid(row=0, column=1, sticky="w", padx=(0, 15), pady=(15, 0))
        
        self.packs = self._get_available_packs()
        self.pack_var = ctk.StringVar(value=self.config.get("sound_pack"))
        self.option_pack = ctk.CTkOptionMenu(self.frame_sound, values=self.packs, variable=self.pack_var, command=self.change_pack, width=150)
        self.option_pack.grid(row=1, column=1, sticky="w", padx=(0, 15), pady=(5, 15))

        # Custom Folder Button (Small link style)
        self.btn_custom = ctk.CTkButton(self.frame_sound, text="📂 Open Custom Folder", command=self.open_custom_folder, 
                                      fg_color="transparent", border_width=0, text_color=("gray50", "gray70"), hover_color=("gray90", "gray30"),
                                      height=24, font=ctk.CTkFont(size=11))
        self.btn_custom.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))


        # --- Card: Audio Controls ---
        self.frame_audio = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color=("gray85", "gray20"))
        self.frame_audio.grid(row=2, column=0, sticky="ew", pady=10)

        # Volume
        self.label_volume = ctk.CTkLabel(self.frame_audio, text="Master Volume", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_volume.pack(anchor="w", padx=15, pady=(15, 0))
        
        self.slider_volume = ctk.CTkSlider(self.frame_audio, from_=0, to=1, command=self.change_volume, progress_color="#1f6aa5")
        self.slider_volume.set(self.config.get("volume"))
        self.slider_volume.pack(fill="x", padx=15, pady=10)

        # Pitch
        self.label_pitch = ctk.CTkLabel(self.frame_audio, text="Sound Variance (Pitch/Vol)", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_pitch.pack(anchor="w", padx=15, pady=(5, 0))

        self.slider_pitch = ctk.CTkSlider(self.frame_audio, from_=0, to=0.2, command=self.change_pitch, progress_color="#1f6aa5")
        self.slider_pitch.set(self.config.get("pitch_variation"))
        self.slider_pitch.pack(fill="x", padx=15, pady=(10, 20))


        # --- Footer / Settings ---
        self.frame_footer = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_footer.grid(row=3, column=0, sticky="ew", pady=20)

        # Start Minimized Checkbox
        self.var_minimized = ctk.BooleanVar(value=self.config.get("start_minimized"))
        self.chk_minimized = ctk.CTkCheckBox(self.frame_footer, text="Start Minimized", variable=self.var_minimized, command=self.toggle_minimized,
                                           font=ctk.CTkFont(size=12))
        self.chk_minimized.pack(side="left")

        # Status
        self.label_status = ctk.CTkLabel(self.frame_footer, text="● ON", text_color="#2cc985", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_status.pack(side="right")

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
