# py-media-toolbox
A collection of Python tools for compressing images, videos, PDFs, converting to AVIF, and audio transcription.

## 1) Files — what each file does

* `clop_like.py`
  **Purpose:** Compress images, videos, and PDFs.
  **Needs:** `Pillow`, `PyMuPDF`, and `ffmpeg` (ffmpeg used for video).

* `convert_to_avif.py`
  **Purpose:** Convert images to AVIF format.
  **Needs:** `Pillow`.

* `transcribe.py`
  **Purpose:** Transcribe `.ogg` audio to text and save to `output.txt`. Default language `ur-PK`.
  **Needs:** `SpeechRecognition`, `pydub` and `ffmpeg` (pydub uses ffmpeg to read audio).

---

## 2) Install Python

* Windows: download and run installer from [https://www.python.org/downloads/](https://www.python.org/downloads/) — **check** “Add Python to PATH” during install.
* macOS: install from python.org or `brew install python`.
* Linux: use distro package manager (`sudo apt install python3 python3-venv python3-pip` on Ubuntu).

Verify:

```bash
# Windows (PowerShell) or macOS/Linux terminal
python --version     # or python3 --version on some systems
pip --version        # or pip3 --version
```

---

## 3) FFmpeg — where to put path (what to paste)

You must add the **ffmpeg `bin` folder** to your PATH so `ffmpeg` command works.

* Example ffmpeg binary location (Windows): `C:\ffmpeg\bin`
  **What to paste into PATH:** `C:\ffmpeg\bin`

* Example ffmpeg location (macOS): `/usr/local/bin` or `/opt/homebrew/bin` (Homebrew path)
  **What to paste into PATH:** `/opt/homebrew/bin` (if that’s where ffmpeg is)

* Example ffmpeg location (Linux): usually `/usr/bin` after `apt install ffmpeg` (already in PATH)

**Windows — add permanently (paste exactly):**

1. Press `Windows`, search **Edit the system environment variables** → Open → Environment Variables.
2. Under **System variables** select `Path` → Edit → New → paste:

```
C:\ffmpeg\bin
```

3. OK, close, open a NEW terminal and run:

```powershell
ffmpeg -version
```

**macOS (if manual):** add line to `~/.zshrc` or `~/.bash_profile`:

```bash
export PATH="/path/to/ffmpeg/bin:$PATH"
```

then `source ~/.zshrc` (or reopen terminal). Verify:

```bash
ffmpeg -version
```

**Linux (Ubuntu):**

```bash
sudo apt update
sudo apt install ffmpeg -y
ffmpeg -version
```

---

## 4) Install all Python packages (copy this block)

**Windows (PowerShell) — single paste:**

```powershell
# create & activate venv (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell. If blocked, run Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# upgrade pip and install packages
pip install --upgrade pip setuptools wheel
pip install Pillow PyMuPDF SpeechRecognition pydub
```

**macOS / Linux — single paste:**

```bash
# create & activate venv
python3 -m venv venv
source venv/bin/activate

# upgrade pip and install packages
pip install --upgrade pip setuptools wheel
pip install Pillow PyMuPDF SpeechRecognition pydub
```

You can also create `requirements.txt` with:

```
Pillow
PyMuPDF
SpeechRecognition
pydub
```

and run:

```bash
pip install -r requirements.txt
```

---

## 5) How to check packages & ffmpeg installed (single commands)

**Check ffmpeg:**

```bash
ffmpeg -version
# You should see version info. If not, PATH not set correctly.
```

**Check Python packages (fast):**

```bash
# Run this in the same terminal where venv is activated (or system python)
python -c "import PIL, fitz, speech_recognition, pydub; print('PACKAGES OK')"
```

* If the line prints `PACKAGES OK` → all installed.
* If it raises `ModuleNotFoundError` → that package did not install.

**Alternative: show versions:**

```bash
pip show Pillow PyMuPDF SpeechRecognition pydub
```

---

## 6) If `pip install` fails — simple troubleshooting

1. Run:

```bash
pip install --upgrade pip setuptools wheel
```

2. Then retry:

```bash
pip install Pillow PyMuPDF SpeechRecognition pydub
```

3. If it still fails:

   * Copy the error message and search or paste here. Common fixes:

     * On Linux, install build tools: `sudo apt install build-essential` (if a C extension needs compiling).
     * If `PyMuPDF` wheel not available, try `pip install pymupdf` (lowercase package name sometimes).
     * Use `--user` to install to your user directory: `pip install --user <package>`.
4. Option: Use prebuilt wheels or use a different Python version (3.8+).

---

## 7) Run commands for each file (examples)

> Use `python` on Windows, `python3` on macOS/Linux if needed. Use quotes around paths with spaces.

**Windows examples:**

```powershell
# Media compressor (compress folder)
python .\clop_like.py "C:\Users\You\Downloads\MyFolder"

# Media compressor, save to another folder
python .\clop_like.py "C:\Users\You\Downloads\Images" --out "C:\Users\You\Downloads\Converted"

# Convert to AVIF
python .\convert_to_avif.py "C:\Users\You\Downloads\MyImages"

# Transcribe OGG to text (default Urdu)
python .\transcribe.py "C:\Users\You\Downloads\audio1.ogg"
```

**macOS / Linux examples:**

```bash
# Media compressor
python3 clop_like.py "/home/you/Downloads/MyFolder"

# Convert to AVIF
python3 convert_to_avif.py "/home/you/Downloads/MyImages"

# Transcribe OGG to text
python3 transcribe.py "/home/you/Downloads/audio1.ogg"
```

Extra options (for `clop_like.py`):

```bash
# set image format, quality, max width, and video crf
python clop_like.py "path" --format webp --quality 60 --max-width 1920 --crf 26
```

---

## 8) How to verify output & that scripts worked

* For `convert_to_avif.py` — check the output folder for files with `.avif` extension.
* For `clop_like.py` — compressed files will be saved next to originals (or in `--out` folder). Check file names end with `_compressed` for videos or have new extension.
* For `transcribe.py` — open `output.txt` in the project folder; you should see the transcription or error messages.

---

## 9) Quick summary checklist (do this one time)

1. Install Python (3.8+). Ensure `python --version` works.
2. Install ffmpeg and add `.../ffmpeg/bin` to PATH. Verify `ffmpeg -version`.
3. Create & activate `venv`.
4. `pip install --upgrade pip setuptools wheel`
5. `pip install Pillow PyMuPDF SpeechRecognition pydub`
6. Test packages: `python -c "import PIL, fitz, speech_recognition, pydub; print('PACKAGES OK')"`
7. Run scripts as shown above.
