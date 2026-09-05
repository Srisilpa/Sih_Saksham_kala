import time
from audio.pipeline import process_audio

cases = [
    "uploads/audio/audio.mp4",
    "uploads/audio/hindi.mp4",
    "uploads/audio/missing.m4a",
    "requirements.txt",
]

for path in cases:
    print("\n===", path, "===")
    start = time.time()
    result = process_audio(path)
    elapsed = round(time.time() - start, 1)

    if result["success"]:
        print("Language :", result["language_name"], f"({result['language']})")
        print("Supported:", result["supported"])
        print("Conf     :", result["confidence"])
        print("Time     :", elapsed, "s")
        print("Text     :", result["text"])
        if result["warning"]:
            print("WARNING  :", result["warning"])
    else:
        print("FAILED   :", result["error"])
import os

os.makedirs("outputs", exist_ok=True)
with open("outputs/transcripts.txt", "w", encoding="utf-8") as f:
    for path in cases:
        r = process_audio(path)
        f.write(f"{path}\n{r.get('text')}\n\n")
print("\nTranscripts written to outputs/transcripts.txt")