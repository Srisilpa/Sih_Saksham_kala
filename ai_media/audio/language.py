SUPPORTED = {
    "en": "English",
    "hi": "Hindi",
}

LOW_CONFIDENCE = 0.7


def check_language(code, confidence):
    """
    Checks a detected language against the supported list.
    Returns a dict describing what was found.
    """

    supported = code in SUPPORTED
    name = SUPPORTED.get(code, code)

    warning = None

    if not supported:
        warning = f"Language '{code}' is outside the supported list (English, Hindi)."
    elif confidence < LOW_CONFIDENCE:
        warning = f"Language detection was uncertain ({confidence})."

    return {
        "language": code,
        "language_name": name,
        "supported": supported,
        "warning": warning,
    }