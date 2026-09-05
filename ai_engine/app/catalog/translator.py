"""
Translator module.
Handles language detection and translation for the multilingual catalog system.
Uses Gemini since it handles Indian regional languages well.
"""

import json
from app.utils.gemini_client import call_gemini


def detect_language(text: str) -> dict:
    """
    Detects the language of the given text.

    Returns:
        dict like {"language_code": "hi", "language_name": "Hindi", "confidence": "high"}
        Falls back to unknown if Gemini fails or response can't be parsed.
    """
    prompt = f"""
Detect the language of this text. The text may be in English, Hindi, Telugu,
Tamil, Kannada, Marathi, Bengali, or another Indian regional language.

Text: "{text}"

Respond ONLY in this exact JSON format, nothing else:
{{"language_code": "<ISO 639-1 code like hi, te, ta, en>", "language_name": "<full language name>", "confidence": "<high or low>"}}
"""

    try:
        raw_response = call_gemini(prompt)
        cleaned = raw_response.strip().strip("`").replace("json", "", 1).strip()
        parsed = json.loads(cleaned)
        return {
            "language_code": parsed.get("language_code", "unknown"),
            "language_name": parsed.get("language_name", "Unknown"),
            "confidence": parsed.get("confidence", "low"),
            "detection_available": True,
        }
    except Exception:
        return {
            "language_code": "unknown",
            "language_name": "Unknown",
            "confidence": "low",
            "detection_available": False,
        }


def translate_text(text: str, target_language: str = "English") -> dict:
    """
    Translates text into the target language (e.g. "English" or "Hindi").

    Returns:
        dict with translated text and a flag showing if AI translation succeeded.
        Falls back to returning the original text untouched if Gemini fails -
        this keeps the pipeline moving even if translation is unavailable.
    """
    prompt = f"""
Translate the following text into {target_language}.
Keep the meaning natural and suitable for an e-commerce product listing.
Do not add any extra commentary.

Text: "{text}"

Respond ONLY in this exact JSON format, nothing else:
{{"translated_text": "<the translation>"}}
"""

    try:
        raw_response = call_gemini(prompt)
        cleaned = raw_response.strip().strip("`").replace("json", "", 1).strip()
        parsed = json.loads(cleaned)
        return {
            "translated_text": parsed.get("translated_text", text),
            "target_language": target_language,
            "translation_available": True,
        }
    except Exception:
        return {
            "translated_text": text,
            "target_language": target_language,
            "translation_available": False,
        }