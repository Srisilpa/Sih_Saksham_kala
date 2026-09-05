"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Loads the trained model and predicts a price for a brand-new product.
This demonstrates how the full pipeline would be used in production,
once real historical data replaces this synthetic dataset.
"""

import pandas as pd
import joblib


def predict_price(
    category: str,
    complexity_level: str,
    region: str,
    season: str,
    material_cost: float,
    labor_cost: float,
) -> float:
    model = joblib.load("models/pricing_model.pkl")
    encoders = joblib.load("models/label_encoders.pkl")
    trends = pd.read_csv("data/price_trends.csv")

    trend_row = trends[(trends["category"] == category) & (trends["season"] == season)]
    trend_multiplier = trend_row["trend_multiplier"].values[0] if not trend_row.empty else 1.0

    base_cost = material_cost + labor_cost

    features = pd.DataFrame([{
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "base_cost": base_cost,
        "trend_multiplier": trend_multiplier,
        "category_encoded": encoders["category"].transform([category])[0],
        "complexity_level_encoded": encoders["complexity_level"].transform([complexity_level])[0],
        "region_encoded": encoders["region"].transform([region])[0],
        "season_encoded": encoders["season"].transform([season])[0],
    }])

    predicted_price = model.predict(features)[0]
    return round(predicted_price, 2)


if __name__ == "__main__":
    price = predict_price(
        category="sarees",
        complexity_level="complex",
        region="West Bengal",
        season="Wedding",
        material_cost=500,
        labor_cost=300,
    )
    print(f"ML-predicted price: rupees {price}")

    # Compare against our REAL rule-based system's answer for the same product
    print("\nFor comparison, ai_engine's real rule-based formula gives:")
    print("(500 + 300) * 1.6 complexity * 1.7 category = rupees 2176.0")