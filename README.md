# Thockify

Thockify is a mechanical keyboard sound simulator for Linux. It plays high-quality (or placeholder) sound effects for every keypress, featuring multiple sound packs and a modern GUI.

## Features
- **Sound Packs:** Choose between Blue, Brown, and Red switch sounds.
- **Custom Sounds:** Load your own folder of `.wav` files.
- **Special Keys:** Distinct sounds for Space, Enter, and Backspace.
- **GUI:** Modern dark-mode interface to control volume and packs.

## Installation

1.  **Prerequisites:** Ensure you have Python 3 installed.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: On some Linux distros, you might need to install `python3-tk` or `python3-devel` via your package manager if `customtkinter` fails).*

## Usage

1.  **Run the App:**
    ```bash
    python main.py
    ```
2.  **Controls:**
    - Use the dropdown to select a sound pack.
    - Use the slider to adjust volume.
    - Click "Open Custom Folder" to add your own sounds.

## Custom Sound Packs
To create a custom pack:
1.  Create a new folder in `assets/` (e.g., `assets/my_switch`).
2.  Add `.wav` files:
    - `base.wav` (Required: used for normal keys)
    - `space.wav`
    - `enter.wav`
    - `backspace.wav`
3.  Restart the app or re-open the dropdown to see your new pack.
