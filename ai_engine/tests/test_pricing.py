"""
Unit tests for the pricing engine.
These test pure business logic only - no real Gemini API calls,
so tests run instantly and never fail due to network/API issues.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pricing import rules
from app.pricing.engine import calculate_rule_based_price


def test_get_labor_cost_uses_artisan_value_when_given():
    result = rules.get_labor_cost("complex", 999)
    assert result == 999


def test_get_labor_cost_falls_back_to_flat_rate():
    result = rules.get_labor_cost("complex", None)
    assert result == 300


def test_get_labor_cost_handles_unknown_complexity():
    result = rules.get_labor_cost("not_a_real_level", None)
    assert result == rules.LABOR_COST_BY_COMPLEXITY["medium"]


def test_get_complexity_multiplier_known_value():
    result = rules.get_complexity_multiplier("very_complex")
    assert result == 2.0


def test_get_complexity_multiplier_unknown_defaults_to_medium():
    result = rules.get_complexity_multiplier("bogus_level")
    assert result == rules.COMPLEXITY_MULTIPLIER["medium"]


def test_get_category_margin_known_value():
    result = rules.get_category_margin("jewelry")
    assert result == 1.6


def test_get_category_margin_unknown_defaults_to_pottery():
    result = rules.get_category_margin("bogus_category")
    assert result == rules.CATEGORY_MARGIN["pottery"]


def test_calculate_rule_based_price_basic_math():
    result = calculate_rule_based_price(
        material_cost=500,
        complexity="complex",
        category="sarees",
    )
    # (500 material + 300 labor) * 1.6 complexity * 1.7 category = 2176.0
    assert result["material_cost"] == 500
    assert result["labor_cost"] == 300
    assert result["base_cost"] == 800
    assert result["complexity_multiplier"] == 1.6
    assert result["category_margin"] == 1.7
    assert result["final_price"] == 2176.0


def test_calculate_rule_based_price_negative_material_cost_clamped_to_zero():
    result = calculate_rule_based_price(
        material_cost=-100,
        complexity="simple",
        category="pottery",
    )
    assert result["material_cost"] == 0


def test_calculate_rule_based_price_uses_artisan_labor_cost_when_given():
    result = calculate_rule_based_price(
        material_cost=200,
        complexity="simple",
        category="pottery",
        artisan_entered_labor_cost=150,
    )
    assert result["labor_cost"] == 150
    # (200 + 150) * 1.0 * 1.4 = 490.0
    assert result["final_price"] == 490.0


def test_all_categories_have_a_margin_defined():
    for category in rules.VALID_CATEGORIES:
        margin = rules.get_category_margin(category)
        assert margin > 0


def test_all_complexity_levels_have_a_multiplier_defined():
    for level in rules.VALID_COMPLEXITY_LEVELS:
        multiplier = rules.get_complexity_multiplier(level)
        assert multiplier > 0