from audio.validate import validate_audio

cases = [
    "uploads/audio/audio.mp4",
    "uploads/audio/hindi.mp4",
    "uploads/audio/missing.m4a",
    "requirements.txt",
    "uploads/images/test1.png",
]

for path in cases:
    result, error = validate_audio(path)
    if error:
        print(f"FAIL  {path}\n      -> {error}")
    else:
        print(f"OK    {path}")