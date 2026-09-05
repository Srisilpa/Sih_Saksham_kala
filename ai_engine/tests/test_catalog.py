"""
Unit tests for the catalog generator.
We test the fallback behavior and structural guarantees without making
real Gemini API calls, so tests stay fast and reliable.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch
from app.catalog.generator import generate_catalog
from app.pricing.rules import VALID_CATEGORIES


def test_generate_catalog_fallback_when_gemini_fails():
    """If Gemini raises an exception, generate_catalog must not crash -
    it should return a safe default structure instead."""
    with patch("app.catalog.generator.call_gemini", side_effect=Exception("API down")):
        result = generate_catalog("some raw artisan description")

    assert result["catalog_ai_available"] is False
    assert result["category"] in VALID_CATEGORIES
    assert isinstance(result["tags"], list)
    assert result["title_en"] != ""
    assert result["description_en"] == "some raw artisan description"


def test_generate_catalog_result_has_all_required_keys():
    with patch("app.catalog.generator.call_gemini", side_effect=Exception("API down")):
        result = generate_catalog("test product")

    required_keys = {
        "title_en", "title_hi", "description_en", "description_hi",
        "category", "tags", "catalog_ai_available",
    }
    assert required_keys.issubset(result.keys())


def test_generate_catalog_success_with_mocked_gemini_response():
    """Simulate a valid Gemini JSON response and confirm it's parsed correctly."""
    fake_response = '''
    {
        "title_en": "Handmade Diya",
        "title_hi": "\\u0939\\u0938\\u094d\\u0924\\u0928\\u093f\\u0930\\u094d\\u092e\\u093f\\u0924 \\u0926\\u0940\\u092f\\u093e",
        "description_en": "A beautiful handmade clay diya.",
        "description_hi": "\\u090f\\u0915 \\u0916\\u0942\\u092c\\u0938\\u0942\\u0930\\u0924 \\u0939\\u0938\\u094d\\u0924\\u0928\\u093f\\u0930\\u094d\\u092e\\u093f\\u0924 \\u092e\\u093f\\u091f\\u094d\\u091f\\u0940 \\u0915\\u093e \\u0926\\u0940\\u092f\\u093e",
        "category": "pottery",
        "tags": ["diya", "clay", "handmade"]
    }
    '''
    with patch("app.catalog.generator.call_gemini", return_value=fake_response):
        result = generate_catalog("mitti ka diya")

    assert result["catalog_ai_available"] is True
    assert result["category"] == "pottery"
    assert result["title_en"] == "Handmade Diya"
    assert "diya" in result["tags"]


def test_generate_catalog_invalid_category_defaults_safely():
    """If Gemini returns a category not in our valid list, we must not
    pass an invalid category downstream to the pricing engine."""
    fake_response = '''
    {
        "title_en": "Something",
        "title_hi": "Something",
        "description_en": "desc",
        "description_hi": "desc",
        "category": "totally_made_up_category",
        "tags": []
    }
    '''
    with patch("app.catalog.generator.call_gemini", return_value=fake_response):
        result = generate_catalog("test")

    assert result["category"] in VALID_CATEGORIES
