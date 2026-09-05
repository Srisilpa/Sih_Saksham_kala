"""
PROTOTYPE / FUTURE SCOPE ONLY
This generates SYNTHETIC (fabricated) historical sales data for demonstration
purposes only. This is NOT real data and is NOT used in the actual SIH
submission's pricing engine (see ai_engine/ for the real, honest system).

Purpose: show what a real ML pricing pipeline would look like once genuine
historical sales data becomes available after the app launches.
"""

import pandas as pd
import numpy as np

np.random.seed(42)  # reproducible results every time this runs

N_ROWS = 2000

CATEGORIES = ["pottery", "textile", "jewelry", "woodwork", "metalwork",
              "bamboo_cane", "sarees", "dress", "home_decor",
              "handmade_food", "bags_accessories"]

COMPLEXITY_LEVELS = ["simple", "medium", "complex", "very_complex"]
COMPLEXITY_WEIGHTS = [0.35, 0.35, 0.2, 0.1]  # simple items are more common

REGIONS = ["Rajasthan", "West Bengal", "Gujarat", "Uttar Pradesh",
           "Tamil Nadu", "Odisha", "Maharashtra"]

SEASONS = ["Diwali", "Wedding", "Regular", "Summer_Festival"]

# Rough base cost ranges per category (rupees) - used to generate believable data
CATEGORY_BASE_MATERIAL_COST = {
    "pottery": (30, 150),
    "textile": (100, 400),
    "jewelry": (150, 600),
    "woodwork": (200, 800),
    "metalwork": (150, 700),
    "bamboo_cane": (40, 200),
    "sarees": (300, 1500),
    "dress": (200, 900),
    "home_decor": (80, 350),
    "handmade_food": (30, 120),
    "bags_accessories": (100, 400),
}

COMPLEXITY_MULTIPLIER = {"simple": 1.0, "medium": 1.3, "complex": 1.6, "very_complex": 2.0}
CATEGORY_MARGIN = {
    "pottery": 1.4, "textile": 1.5, "jewelry": 1.6, "woodwork": 1.5,
    "metalwork": 1.5, "bamboo_cane": 1.3, "sarees": 1.7, "dress": 1.6,
    "home_decor": 1.4, "handmade_food": 1.3, "bags_accessories": 1.5,
}
SEASON_DEMAND_BOOST = {"Diwali": 1.15, "Wedding": 1.20, "Regular": 1.0, "Summer_Festival": 1.05}


def generate_row(product_id):
    category = np.random.choice(CATEGORIES)
    complexity = np.random.choice(COMPLEXITY_LEVELS, p=COMPLEXITY_WEIGHTS)
    region = np.random.choice(REGIONS)
    season = np.random.choice(SEASONS)

    material_low, material_high = CATEGORY_BASE_MATERIAL_COST[category]
    material_cost = round(np.random.uniform(material_low, material_high), 2)
    labor_cost = round(material_cost * np.random.uniform(0.3, 0.7), 2)

    base_cost = material_cost + labor_cost
    price_before_noise = (
        base_cost
        * COMPLEXITY_MULTIPLIER[complexity]
        * CATEGORY_MARGIN[category]
        * SEASON_DEMAND_BOOST[season]
    )

    # Add realistic random noise (+/- 10%) to simulate real-world price variation
    noise_factor = np.random.uniform(0.9, 1.1)
    final_selling_price = round(price_before_noise * noise_factor, 2)

    return {
        "product_id": f"P{product_id:05d}",
        "category": category,
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "complexity_level": complexity,
        "region": region,
        "season": season,
        "final_selling_price": final_selling_price,
    }


def main():
    rows = [generate_row(i) for i in range(1, N_ROWS + 1)]
    df = pd.DataFrame(rows)

    output_path = "data/synthetic_sales_data.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} synthetic rows")
    print(f"Saved to: {output_path}")
    print("\nSample rows:")
    print(df.head())
    print("\nCategory distribution:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()