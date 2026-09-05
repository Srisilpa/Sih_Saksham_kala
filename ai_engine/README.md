# AI Engine - Team 5 (LLM Engine + Dynamic Pricing)

This module is the "brain" of the Virtual Business Manager app. It takes an
artisan's raw product description (from voice-to-text) and cost inputs, and
returns a complete, e-commerce-ready product listing with a suggested price.

It does NOT handle databases, user accounts, images, or audio processing -
those belong to Teams 3 and 4. This module only takes clean text/data in,
and returns clean text/data out.

## What this module does

1. Multilingual Catalog Generation - turns a rough spoken description
   (in Hindi, Hinglish, or English) into a professional title, description,
   category, and tags - in both English and Hindi.
2. Dynamic Pricing - calculates a fair price using a hybrid approach:
   a transparent rule-based formula (material cost + labor + complexity +
   category margin), then a small AI adjustment (max +/-15%) with a
   plain-language explanation.
3. Translation and Language Detection - detects the language of input text
   and translates between English and Hindi.

Every AI-powered function has a safe fallback. If the Gemini API fails, is
rate-limited, or the quota runs out, this module still returns a usable
result - it never crashes the pipeline.

## Folder structure

ai_engine/
  app/
    main.py              - Main entry point - process_product_listing()
    catalog/
      generator.py       - Title/description/tags/category generation
      translator.py      - Language detection + translation
    pricing/
      rules.py           - Hardcoded pricing rules (no AI)
      engine.py          - Rule-based price + Gemini adjustment
    models/
      schemas.py         - Shared data contracts (Pydantic models)
    utils/
      gemini_client.py   - Shared Gemini API wrapper with retry logic
  tests/                 - 16 unit tests, no live API calls needed
  demo_cache/
    sample_responses.json - Pre-verified responses for offline-safe demos
  requirements.txt

## Setup (for teammates)

cd ai_engine
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

Create a .env file in this folder (copy .env.example) and add your own
Gemini API key:

GEMINI_API_KEY=your_key_here

Get a free key at: https://aistudio.google.com/app/apikey

Note: the free tier allows only 20 requests/day. For live demos, use the
demo_cache_key parameter (see below) to avoid hitting this limit.

## How Team 3 should use this module

Import and call the single entry point:

from app.main import process_product_listing

result = process_product_listing(
    raw_text="yeh mitti ka bana hua diya hai, hath se banaya",
    material_cost=80,
    complexity="medium",
    artisan_entered_labor_cost=None,
    image_tags=None,
)

Returns a dict with two keys: catalog (title/description/tags/category in
English and Hindi) and pricing (rule-based price, AI-adjusted price, and
a plain-language explanation).

### For live demos (recommended)

Skip live Gemini calls entirely and get an instant, guaranteed response:

result = process_product_listing(
    raw_text="", material_cost=0, complexity="medium",
    demo_cache_key="diya"
)

## Valid values

Complexity levels: simple, medium, complex, very_complex

Categories: pottery, textile, jewelry, woodwork, metalwork, bamboo_cane,
sarees, dress, home_decor, handmade_food, bags_accessories

## Running tests

pytest -v

16 tests covering pricing math and catalog fallback behavior. No live API
calls are made during testing, so tests run instantly and never fail due
to network or quota issues.

## Design decisions worth knowing

- Pricing is never AI-only. The rule-based formula always runs first and
  is always a valid, explainable price on its own. Gemini can only nudge
  it by +/-15% - it can never replace it.
- Category is decided once, in the catalog generator, and reused for
  pricing - so the same product is never categorized inconsistently
  between listing and pricing.
- All Gemini calls retry automatically (up to 3 attempts) before falling
  back, since temporary 503 errors are common on the free tier.
