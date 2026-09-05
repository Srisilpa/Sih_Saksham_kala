"""
Pricing rules for the Dynamic Pricing Engine.
These are hardcoded business rules — no AI involved here.
This file must work standalone, even if Gemini API is completely down.
"""

# Flat labor cost estimate (in ₹) used ONLY if artisan doesn't enter their own cost
LABOR_COST_BY_COMPLEXITY = {
    "simple": 50,
    "medium": 150,
    "complex": 300,
    "very_complex": 500,
}

# Multiplier applied on top of (material + labor) cost, based on how fiddly the craft is
COMPLEXITY_MULTIPLIER = {
    "simple": 1.0,
    "medium": 1.3,
    "complex": 1.6,
    "very_complex": 2.0,
}

# Category-specific margin multiplier — reflects typical market markup per craft type
CATEGORY_MARGIN = {
    "pottery": 1.4,
    "textile": 1.5,
    "jewelry": 1.6,
    "woodwork": 1.5,
    "metalwork": 1.5,
    "bamboo_cane": 1.3,
    "sarees": 1.7,
    "dress": 1.6,
    "home_decor": 1.4,
    "handmade_food": 1.3,
    "bags_accessories": 1.5,
}
VALID_COMPLEXITY_LEVELS = list(COMPLEXITY_MULTIPLIER.keys())
VALID_CATEGORIES = list(CATEGORY_MARGIN.keys())


def get_labor_cost(complexity: str, artisan_entered_cost: float | None) -> float:
    """
    Returns the labor cost to use in pricing.
    Prefers the artisan's own entered cost; falls back to flat rate by complexity.
    """
    if artisan_entered_cost is not None and artisan_entered_cost > 0:
        return artisan_entered_cost

    if complexity not in LABOR_COST_BY_COMPLEXITY:
        complexity = "medium"  # safe default if invalid/missing value comes in

    return LABOR_COST_BY_COMPLEXITY[complexity]


def get_complexity_multiplier(complexity: str) -> float:
    """Returns the complexity multiplier, defaulting to 'medium' if unknown."""
    return COMPLEXITY_MULTIPLIER.get(complexity, COMPLEXITY_MULTIPLIER["medium"])


def get_category_margin(category: str) -> float:
    """Returns the category margin multiplier, defaulting to 'pottery' if unknown."""
    return CATEGORY_MARGIN.get(category, CATEGORY_MARGIN["pottery"])