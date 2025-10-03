#!/usr/bin/env python3
"""
Simple, robust media compressor:
- Images: tries requested format, falls back to WEBP then JPEG
- Videos: uses ffmpeg (libx265) with configurable CRF
- PDFs: uses PyMuPDF (fitz) with deflate + garbage collection

Usage examples:
  python media_compressor.py path/to/file.jpg
  python media_compressor.py path/to/folder --out converted --format avif --quality 60 --max-width 1920
  python media_compressor.py file1.jpg file2.png --out ./out --format webp
"""

import os
import sys
import argparse
import subprocess
import shutil
from PIL import Image
import fitz  # PyMuPDF

import re

def safe_filename(name, max_length=100):
    # Non-alphanumeric ko underscore me badal do
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Agar naam bohot lamba hai to cut kar do
    return name[:max_length]

def compress_image(input_path, output_folder=None, quality=50, max_width=None, out_format="avif"):
    try:
        img = Image.open(input_path).convert("RGB")
    except Exception as e:
        print(f"❌ Cannot open image {input_path}: {e}")
        return

    # Resize if requested
    if max_width and img.width > max_width:
        new_h = int(img.height * (max_width / img.width))
        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)

    # ✅ SAFE FILE NAME BANADO
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    base_name = safe_filename(base_name)

    dest_folder = output_folder or os.path.dirname(input_path)
    os.makedirs(dest_folder, exist_ok=True)

    requested = out_format.lower()
    ordered = []
    if requested not in ordered:
        ordered.append(requested)
    if "webp" not in ordered:
        ordered.append("webp")
    if "jpg" not in ordered and "jpeg" not in ordered:
        ordered.append("jpg")

    last_exc = None
    for fmt in ordered:
        fmt_upper = "JPEG" if fmt in ("jpg", "jpeg") else fmt.upper()
        out_ext = "jpg" if fmt in ("jpg", "jpeg") else fmt
        out_path = os.path.join(dest_folder, f"{base_name}.{out_ext}")
        try:
            img.save(out_path, fmt_upper, quality=quality)
            print(f"✅ Image saved: {out_path} ({fmt_upper})")
            return
        except Exception as e:
            last_exc = e
    print(f"❌ Failed to save image {input_path}. Last error: {last_exc}")


def compress_video(input_path, output_folder=None, crf=28):
    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg not found in PATH. Install ffmpeg to enable video compression.")
        return

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    dest_folder = output_folder or os.path.dirname(input_path)
    os.makedirs(dest_folder, exist_ok=True)
    out_path = os.path.join(dest_folder, f"{base_name}_compressed.mp4")

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vcodec", "libx265", "-crf", str(crf),
        "-preset", "medium",  # balance speed & size
        out_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Video compressed: {out_path}")
        else:
            print(f"❌ Video compression failed for {input_path}.\nffmpeg stderr:\n{result.stderr.strip()}")
    except Exception as e:
        print(f"❌ Error running ffmpeg for {input_path}: {e}")

def compress_pdf(input_path, output_folder=None):
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"❌ Cannot open PDF {input_path}: {e}")
        return

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    dest_folder = output_folder or os.path.dirname(input_path)
    os.makedirs(dest_folder, exist_ok=True)
    out_path = os.path.join(dest_folder, f"{base_name}_compressed.pdf")

    try:
        # simple save with garbage collection and deflate
        doc.save(out_path, deflate=True, garbage=4)
        doc.close()
        print(f"✅ PDF compressed: {out_path}")
    except Exception as e:
        print(f"❌ Failed to save compressed PDF {input_path}: {e}")

def process_path(path, output_folder=None, out_format="avif", quality=50, max_width=None, crf=28):
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp", ".avif"]:
            compress_image(path, output_folder, quality=quality, max_width=max_width, out_format=out_format)
        elif ext in [".mp4", ".mov", ".mkv", ".avi", ".webm"]:
            compress_video(path, output_folder, crf=crf)
        elif ext == ".pdf":
            compress_pdf(path, output_folder)
        else:
            print(f"⚠️ Skipping unsupported file type: {path}")
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                file_path = os.path.join(root, f)
                # avoid processing files inside output folder when user sets output inside input
                if output_folder:
                    try:
                        # normalize and compare
                        if os.path.commonpath([os.path.abspath(output_folder)]) == os.path.commonpath([os.path.abspath(output_folder), os.path.abspath(file_path)]):
                            # file is inside output folder -> skip to avoid loops
                            continue
                    except Exception:
                        pass
                process_path(file_path, output_folder, out_format, quality, max_width, crf)
    else:
        print(f"⚠️ Path not found: {path}")

def main():
    parser = argparse.ArgumentParser(description="Compress images, videos and PDFs (simple & robust).")
    parser.add_argument("paths", nargs="+", help="File(s) or folder(s) to process")
    parser.add_argument("--out", "-o", help="Output folder (optional). If not given, saves beside original files.")
    parser.add_argument("--format", "-f", default="avif", help="Image output format preference (avif, webp, jpg). Default: avif")
    parser.add_argument("--quality", "-q", type=int, default=50, help="Quality for images (1-95). Default: 50")
    parser.add_argument("--max-width", type=int, default=None, help="Max width for images (resize if wider).")
    parser.add_argument("--crf", type=int, default=28, help="CRF for video compression (lower = better quality). Default: 28")

    args = parser.parse_args()

    # ✅ Agar output folder diya gaya hai, aur exist nahi karta to bana do
    if args.out:
        os.makedirs(args.out, exist_ok=True)

    # Validate basic things
    if args.format.lower() not in ("avif", "webp", "jpg", "jpeg"):
        print("⚠️ Unsupported image format preference. Use avif, webp or jpg. Falling back to avif.")
        args.format = "avif"

    for p in args.paths:
        process_path(p, args.out, args.format.lower(), args.quality, args.max_width, args.crf)

if __name__ == "__main__":
    main()


# =============================
# 💻 USAGE EXAMPLES
# =============================

# 1️⃣ Folder ke saare images convert karna (same folder me save, default AVIF):
# python clop_like.py "C:\Users\SMR\Downloads\MyFolder"

# 2️⃣ Folder ke saare images convert karke dusre folder me save karna (default AVIF):
# python clop_like.py "C:\Users\SMR\Downloads\Images\image" --out "C:\Users\SMR\Downloads\Images\Ready_image"

# 3️⃣ Folder ke images convert karke dusre folder me save karna + JPG format:
# python clop_like.py "C:\Users\SMR\Downloads\MyFolder" --out "C:\Users\SMR\Downloads\Converted" --format jpg

# 4️⃣ Specific images convert karna (same folder me save, default AVIF):
# python clop_like.py "C:\Users\SMR\Downloads\img1.jpg" "C:\Users\SMR\Downloads\img2.png"

# 5️⃣ Specific images convert karna + alag folder + AVIF:
# python clop_like.py "C:\Users\SMR\Downloads\img1.jpg" "C:\Users\SMR\Downloads\img2.png" --out "C:\Users\SMR\Downloads\Converted" --format avif

# 6️⃣ Specific images convert karna + alag folder + JPG:
# python clop_like.py "C:\Users\SMR\Downloads\img1.png" "C:\Users\SMR\Downloads\img2.bmp" --out "C:\Users\SMR\Downloads\Converted" --format jpg

# 7️⃣ Folder ke saare files convert karna + JPG:
# python clop_like.py "C:\Users\SMR\Downloads\MyFolder" --format jpg
