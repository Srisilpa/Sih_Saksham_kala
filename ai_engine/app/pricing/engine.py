"""
Pricing Engine — combines rule-based logic (from rules.py) into a final price.
This works completely offline/without AI. Gemini adjustment (if used) happens
in a separate layer on TOP of this, never replacing it.
"""

from app.pricing import rules


def calculate_rule_based_price(
    material_cost: float,
    complexity: str,
    category: str,
    artisan_entered_labor_cost: float | None = None,
) -> dict:
    """
    Calculates a price using pure business rules, no AI involved.

    Args:
        material_cost: cost of raw materials, entered by artisan (in ₹)
        complexity: one of rules.VALID_COMPLEXITY_LEVELS
        category: one of rules.VALID_CATEGORIES
        artisan_entered_labor_cost: optional, artisan's own labor cost estimate

    Returns:
        dict with the final price and a breakdown, so the artisan/judge
        can see exactly how the number was calculated.
    """
    if material_cost < 0:
        material_cost = 0

    labor_cost = rules.get_labor_cost(complexity, artisan_entered_labor_cost)
    complexity_multiplier = rules.get_complexity_multiplier(complexity)
    category_margin = rules.get_category_margin(category)

    base_cost = material_cost + labor_cost
    price_after_complexity = base_cost * complexity_multiplier
    final_price = price_after_complexity * category_margin

    return {
        "material_cost": round(material_cost, 2),
        "labor_cost": round(labor_cost, 2),
        "base_cost": round(base_cost, 2),
        "complexity_multiplier": complexity_multiplier,
        "category_margin": category_margin,
        "final_price": round(final_price, 2),
    }
import json
from app.utils.gemini_client import call_gemini


def get_ai_adjusted_price(
    rule_based_result: dict,
    product_description: str,
    category: str,
) -> dict:
    """
    Takes the rule-based price and asks Gemini to suggest a small adjustment
    (max +/-15%) based on the product description and market context.

    If Gemini fails for any reason, falls back to the rule-based price
    with a note explaining AI adjustment was unavailable.
    """
    base_price = rule_based_result["final_price"]
    min_price = round(base_price * 0.85, 2)
    max_price = round(base_price * 1.15, 2)

    prompt = f"""
You are a pricing assistant for handmade artisan products in India.

Product category: {category}
Product description: {product_description}
Rule-based calculated price: rupees {base_price}
Allowed adjustment range: rupees {min_price} to rupees {max_price} (max 15% up or down)

Task: Suggest a final selling price within the allowed range, and explain
why in 1-2 short sentences a rural artisan can understand.

Respond ONLY in this exact JSON format, nothing else:
{{"suggested_price": <number>, "explanation": "<short explanation>"}}
"""

    try:
        raw_response = call_gemini(prompt)
        cleaned = raw_response.strip().strip("`").replace("json", "", 1).strip()
        parsed = json.loads(cleaned)

        suggested_price = float(parsed["suggested_price"])
        suggested_price = max(min_price, min(max_price, suggested_price))

        return {
            **rule_based_result,
            "ai_adjusted_price": round(suggested_price, 2),
            "ai_explanation": parsed.get("explanation", ""),
            "ai_available": True,
        }

    except Exception:
        return {
            **rule_based_result,
            "ai_adjusted_price": rule_based_result["final_price"],
            "ai_explanation": "AI price suggestion is currently unavailable. Showing standard calculated price.",
            "ai_available": False,
        }