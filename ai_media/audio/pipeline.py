from audio.validate import validate_audio
from audio.transcribe import transcribe_audio
from audio.language import check_language


def _fail(message):
    """Builds a failure response."""
    return {
        "success": False,
        "text": None,
        "language": None,
        "language_name": None,
        "supported": False,
        "confidence": 0.0,
        "warning": None,
        "error": message
    }


def process_audio(input_path):
    """
    Full audio pipeline for artisan voice recordings.

    Input:  path to the uploaded audio file
    Output: dict with success, text, language, and error
    """

    checked_path, error = validate_audio(input_path)
    if error:
        return _fail(error)

    result, error = transcribe_audio(checked_path)
    if error:
        return _fail(error)

    text = result["text"]

    if not text:
        return _fail("No speech detected. Please record again and speak clearly.")

    lang = check_language(result["language"], result["confidence"])

    return {
        "success": True,
        "text": text,
        "language": lang["language"],
        "language_name": lang["language_name"],
        "supported": lang["supported"],
        "confidence": result["confidence"],
        "warning": lang["warning"],
        "error": None
    }