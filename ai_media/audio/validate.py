import os

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"}

MIN_BYTES = 2000
MAX_BYTES = 25 * 1024 * 1024


def validate_audio(path):
    """
    Checks if an audio file is safe to send to Whisper.
    Returns (path, error_message).
    On success, error_message is None.
    """

    if not os.path.exists(path):
        return None, "Audio file not found"

    extension = os.path.splitext(path)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        return None, f"Unsupported audio format '{extension}'. Allowed: {allowed}"

    size = os.path.getsize(path)

    if size < MIN_BYTES:
        return None, "Recording is too short or empty. Please record again."

    if size > MAX_BYTES:
        mb = round(size / (1024 * 1024), 1)
        return None, f"Recording too large ({mb} MB). Maximum is 25 MB."

    return path, None