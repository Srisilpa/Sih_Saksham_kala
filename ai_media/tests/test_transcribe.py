import time
from audio.validate import validate_audio
from audio.transcribe import transcribe_audio

files = [
    "uploads/audio/audio.mp4",
    "uploads/audio/hindi.mp4",
]

for path in files:
    print("\n===", path, "===")

    checked, error = validate_audio(path)
    if error:
        print("Validation failed:", error)
        continue

    start = time.time()
    result, error = transcribe_audio(checked)
    elapsed = round(time.time() - start, 1)

    if error:
        print("Failed:", error)
    else:
        print("Language  :", result["language"])
        print("Confidence:", result["confidence"])
        print("Time      :", elapsed, "seconds")
        print("Text      :", result["text"])