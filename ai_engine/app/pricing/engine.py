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