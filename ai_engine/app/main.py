"""
Main integration entry point for Team 5's AI Engine.
Team 3 should primarily use process_product_listing() below - it ties
together catalog generation and pricing into a single call.
"""

import json
import os

from app.catalog.generator import generate_catalog
from app.pricing.engine import calculate_rule_based_price, get_ai_adjusted_price

_DEMO_CACHE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "demo_cache", "sample_responses.json"
)


def _load_demo_cache() -> dict:
    """Loads the pre-generated demo responses from disk."""
    with open(_DEMO_CACHE_PATH, encoding="utf-8") as f:
        return json.load(f)


def process_product_listing(
    raw_text: str,
    material_cost: float,
    complexity: str,
    artisan_entered_labor_cost: float | None = None,
    image_tags: list[str] | None = None,
    demo_cache_key: str | None = None,
) -> dict:
    """
    Full pipeline: takes an artisan's raw description and cost inputs,
    and returns a complete catalog + pricing result ready to show the
    artisan for review, or to save as a product listing.

    Args:
        raw_text: artisan's spoken product description (voice-to-text output)
        material_cost: cost of raw materials in rupees
        complexity: one of "simple", "medium", "complex", "very_complex"
        artisan_entered_labor_cost: optional, artisan's own labor estimate
        image_tags: optional tags detected from the product image
        demo_cache_key: OPTIONAL. If provided (e.g. "diya" or "saree"),
            skips live Gemini calls entirely and returns a pre-verified
            real response instantly. Use this during live demos to avoid
            any risk of API quota limits or network issues on stage.

    Returns:
        dict combining catalog info (title/description/tags/category) and
        pricing info (rule-based price + AI-adjusted price + explanation).
    """
    if demo_cache_key is not None:
        cache = _load_demo_cache()
        if demo_cache_key in cache:
            return cache[demo_cache_key]
        # if an unknown key is passed, fall through to live generation below

    catalog = generate_catalog(raw_text=raw_text, image_tags=image_tags)

    rule_based_result = calculate_rule_based_price(
        material_cost=material_cost,
        complexity=complexity,
        category=catalog["category"],
        artisan_entered_labor_cost=artisan_entered_labor_cost,
    )

    pricing_result = get_ai_adjusted_price(
        rule_based_result=rule_based_result,
        product_description=catalog["description_en"],
        category=catalog["category"],
    )

    return {
        "catalog": catalog,
        "pricing": pricing_result,
    }