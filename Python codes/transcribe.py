import argparse
import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe(file_path, lang="ur-PK", mode="single"):
    recognizer = sr.Recognizer()

    try:
        # Convert OGG to WAV
        sound = AudioSegment.from_file(file_path, format="ogg")
        wav_file = file_path.replace(".ogg", ".wav")
        sound.export(wav_file, format="wav")

        # Speech recognition
        with sr.AudioFile(wav_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=lang)

            # File name extract
            file_name = os.path.basename(file_path)

            # Decide write mode
            write_mode = "w" if mode == "single" else "a"

            with open("output.txt", write_mode, encoding="utf-8") as f:
                f.write(f"File: {file_name}\n\n{text}\n\n")

    except Exception as e:
        file_name = os.path.basename(file_path)
        write_mode = "w" if mode == "single" else "a"
        with open("output.txt", write_mode, encoding="utf-8") as f:
            f.write(f"File: {file_name}\n\n⚠️ Error: {e}\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio to Text Converter")
    parser.add_argument("files", nargs="+", help="Path(s) to your OGG audio file(s)")
    parser.add_argument("--lang", default="ur-PK", help="Language code (default: ur-PK)")
    args = parser.parse_args()

    # Agar ek file hai → overwrite karega
    if len(args.files) == 1:
        transcribe(args.files[0], args.lang, mode="single")
    else:
        # Multiple files → append karega
        for f in args.files:
            transcribe(f, args.lang, mode="multi")



# Usage Examples

# 1) Single File
# python transcribe.py "C:\Users\SMR\Downloads\audio1.ogg"

# 2) Multiple Files
# python transcribe.py "C:\Users\SMR\Downloads\audio1.ogg" "C:\Users\SMR\Downloads\audio2.ogg"

