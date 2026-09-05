import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from faster_whisper import WhisperModel

MODEL_SIZE = "models/whisper-base"

_model = None


def get_model():
    """Loads the Whisper model once and reuses it."""
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


def transcribe_audio(path):
    """
    Converts speech in an audio file to text.
    Input:  path to a validated audio file
    Output: (result_dict, error_message)
    """
    try:
        model = get_model()

        segments, info = model.transcribe(path, beam_size=5)

        pieces = []
        for segment in segments:
            pieces.append(segment.text)

        text = " ".join(pieces).strip()

        result = {
            "text": text,
            "language": info.language,
            "confidence": round(info.language_probability, 2)
        }

        return result, None

    except Exception as e:
        return None, f"Transcription failed: {e}"