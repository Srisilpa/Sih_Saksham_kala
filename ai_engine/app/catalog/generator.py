"""
Catalog Generator.
Takes a raw product description (from voice-to-text) and generates a full
e-commerce-ready catalog entry: title, description, category, tags -
in both English and Hindi.
"""

import json
from app.utils.gemini_client import call_gemini
from app.pricing.rules import VALID_CATEGORIES


def generate_catalog(raw_text: str, image_tags: list[str] | None = None) -> dict:
    """
    Generates a full product catalog entry from raw artisan input.

    Args:
        raw_text: the artisan's spoken description (already transcribed to text,
                   may be in Hindi/regional language or Hinglish)
        image_tags: optional list of tags detected from the product image
                    (e.g. from Team 4's vision pipeline), used as extra context

    Returns:
        dict with title/description in English and Hindi, category, and tags.
        Falls back to a simple template if Gemini fails, so the pipeline
        never breaks even if AI is unavailable.
    """
    image_context = ""
    if image_tags:
        image_context = f"\nImage tags detected: {', '.join(image_tags)}"

    categories_list = ", ".join(VALID_CATEGORIES)

    prompt = f"""
You are helping an Indian artisan create an e-commerce product listing.
The artisan described their product in their own words, possibly in Hindi,
a regional language, or a mix (Hinglish). Turn this into a professional listing.

Artisan's description: "{raw_text}"{image_context}

Choose the category from ONLY this list: {categories_list}

Generate:
1. A short, appealing product title (English and Hindi)
2. A 2-3 sentence professional product description (English and Hindi),
   suitable for an e-commerce listing, highlighting handmade/craft value
3. The single best-fit category from the list above
4. 4-6 relevant tags for search/SEO (English, lowercase, single words or short phrases)

Respond ONLY in this exact JSON format, nothing else:
{{
  "title_en": "...",
  "title_hi": "...",
  "description_en": "...",
  "description_hi": "...",
  "category": "...",
  "tags": ["...", "..."]
}}
"""

    try:
        raw_response = call_gemini(prompt)
        cleaned = raw_response.strip().strip("`").replace("json", "", 1).strip()
        parsed = json.loads(cleaned)

        category = parsed.get("category", "").lower().replace(" ", "_")
        if category not in VALID_CATEGORIES:
            category = "home_decor"  # safe default if AI picks something unexpected

        return {
            "title_en": parsed.get("title_en", "Handmade Product"),
            "title_hi": parsed.get("title_hi", "हस्तनिर्मित उत्पाद"),
            "description_en": parsed.get("description_en", raw_text),
            "description_hi": parsed.get("description_hi", raw_text),
            "category": category,
            "tags": parsed.get("tags", []),
            "catalog_ai_available": True,
        }

    except Exception:
        return {
            "title_en": "Handmade Product",
            "title_hi": "हस्तनिर्मित उत्पाद",
            "description_en": raw_text,
            "description_hi": raw_text,
            "category": "home_decor",
            "tags": ["handmade"],
            "catalog_ai_available": False,
        }