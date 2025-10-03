import sys
import os
from PIL import Image

def convert_images_to_avif(input_files, output_folder=None):
    valid_files = []
    for file_path in input_files:
        if os.path.isfile(file_path):
            try:
                Image.open(file_path)  # check if it's image
                valid_files.append(file_path)
            except:
                pass
        elif os.path.isdir(file_path):  # if it's a folder
            for f in os.listdir(file_path):
                full_path = os.path.join(file_path, f)
                try:
                    Image.open(full_path)
                    valid_files.append(full_path)
                except:
                    pass

    if not valid_files:
        print("⚠️ No valid images found!")
        return

    for file_path in valid_files:
        try:
            img = Image.open(file_path).convert("RGB")
            folder, filename = os.path.split(file_path)
            name, _ = os.path.splitext(filename)

            save_folder = output_folder if output_folder else folder
            os.makedirs(save_folder, exist_ok=True)

            save_path = os.path.join(save_folder, f"{name}.avif")
            img.save(save_path, "AVIF")
            print(f"✅ {file_path} → {save_path}")
        except Exception as e:
            print(f"❌ Error converting {file_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert_to_avif.py <folder>")
        print("  python convert_to_avif.py <folder> <output_folder>")
        print("  python convert_to_avif.py <file1> <file2> ... <output_folder(optional)>")
        sys.exit(1)

    *inputs, last = sys.argv[1:]
    if os.path.exists(last):  
        # last argument is path, not output folder
        inputs = sys.argv[1:]
        output_folder = None
    else:
        # last argument is output folder
        inputs = sys.argv[1:-1]
        output_folder = last

    convert_images_to_avif(inputs, output_folder)


# Example Commands (Terminal)
# =============================

# 1. Folder me sari images convert karna (same folder me save):
# python convert_to_avif.py "C:\Users\SMR\Downloads\MyImages"

# 2. Folder se convert karke dusre folder me save karna:
# python convert_to_avif.py "C:\Users\SMR\Downloads\MyImages" "C:\Users\SMR\Downloads\Converted_AVIF"

# 3. Specific images convert karna:
# C:\Users\SMR\Downloads\WhatsApp Unknown 2025-09-26 at 4.30.32 PM

# 4. Specific images convert karke alag folder me save karna:
# python convert_to_avif.py "C:\Users\SMR\Downloads\img1.jpg" "C:\Users\SMR\Downloads\img2.png" "C:\Users\SMR\Downloads\Converted_AVIF"