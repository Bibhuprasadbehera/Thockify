import os
import shutil
import json

def import_pack(source_path, dest_path):
    print(f"Importing from {source_path} to {dest_path}...")
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)

    # 1. Clean existing placeholders if any
    for f in os.listdir(dest_path):
        os.remove(os.path.join(dest_path, f))

    # 2. Determine where the files are
    # Some packs are flat (nk-cream)
    # Some packs are nested: mxblue-travel/press/GENERIC_R0.mp3
    
    search_path = source_path
    if os.path.exists(os.path.join(source_path, "press")):
        search_path = os.path.join(source_path, "press")
        print(f"  Found 'press' subdirectory, using that.")

    files = os.listdir(search_path)
    
    # helper to copy with new name
    def copy_sound(src_filename, dst_filename):
        # file extension might be .wav or .mp3
        full_src = os.path.join(search_path, src_filename)
        ext = os.path.splitext(src_filename)[1]
        full_dst = os.path.join(dest_path, dst_filename + ext)  # Keep original extension? 
        # Thockify sound engine needs to be robust to extension. 
        # Or we rename everything to .wav if we used ffmpeg, but for now let's just keep extension
        # and assume sound engine loads it (pygame supports mp3/wav/ogg).
        
        # Actually, let's normalize to .wav suffix for the engine's assumption 
        # OR update the engine. Updating engine is cleaner, but for now 
        # let's just copy exactly.
        
        # WAIT: The SoundEngine looks for "base.wav". If we copy "GENERIC.mp3" to "base.mp3", 
        # SoundEngine won't load it unless we update SoundEngine.
        # Let's rename to .wav extension for simplicity if pygame can handle it (it uses file header usually)
        # BUT standard practice is to respect extension.
        # Let's try to copy to `base.wav` even if it is an mp3 content. Pygame mixer usually autodetects.
        
        shutil.copy2(full_src, os.path.join(dest_path, dst_filename + ".wav"))
        print(f"  Copied {src_filename} -> {dst_filename}.wav")

    # 3. Find Base Sound
    # Candidates: 'a.wav', 'GENERIC_R0.mp3', '1.wav'
    candidates = [
        "a.wav", "a.mp3", 
        "GENERIC_R0.mp3", "GENERIC_R0.wav",
        "1.wav", "1.mp3",
        "q.wav", "q.mp3"
    ]
    
    base_found = False
    for cand in candidates:
        if cand in files:
            copy_sound(cand, "base")
            base_found = True
            break
            
    if not base_found:
        # Fallback: any file starting with GENERIC or any single letter
        for f in files:
            if f.startswith("GENERIC") or len(os.path.splitext(f)[0]) == 1:
                copy_sound(f, "base")
                base_found = True
                break

    if not base_found:
        print("  Error: Could not find base sound.")

    # 4. Find Specials
    # Candidates for space: 'space.wav', 'SPACE.mp3', etc
    specials_map = {
        "space": ["space.wav", "space.mp3", "SPACE.mp3", "SPACE.wav"],
        "enter": ["enter.wav", "enter.mp3", "ENTER.mp3", "ENTER.wav"],
        "backspace": ["backspace.wav", "backspace.mp3", "BACKSPACE.mp3", "BACKSPACE.wav"]
    }

    for key, opts in specials_map.items():
        found = False
        for opt in opts:
            if opt in files:
                copy_sound(opt, key)
                found = True
                break
        if not found and base_found:
             # If special missing, valid behavior is just strictly missing 
             # (engine falls back to base), or we can duplicate base.
             # Engine handles missing fine.
             pass

def main():
    root = os.getcwd()
    mechvibes_audio = os.path.join(root, "temp_mechvibes2", "src", "audio")
    assets_dir = os.path.join(root, "assets")
    
    # Mapping: Source Folder Name -> Target Thockify Asset Name
    # We replace our placeholders (blue, brown, red) with real recordings
    mappings = {
        "mxblue-travel": "blue",
        "mxbrown-travel": "brown",
        "mxblack-travel": "red",          # Using black (linear) for red
        "nk-cream": "cream",              # New pack!
        "holy-pandas": "holy_pandas",     # New pack!
        "turquoise": "turquoise"          # New pack!
    }
    
    for src_name, target_name in mappings.items():
        src = os.path.join(mechvibes_audio, src_name)
        dst = os.path.join(assets_dir, target_name)
        
        if os.path.exists(src):
            import_pack(src, dst)
        else:
            print(f"Skipping {src_name} - not found.")

if __name__ == "__main__":
    main()
