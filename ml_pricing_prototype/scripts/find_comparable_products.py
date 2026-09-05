"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Finds comparable historical products for a new product, based on category,
complexity, and similar material cost. This mimics how a real pricing system
would look up "what did similar products sell for" before suggesting a price.
"""

import pandas as pd


def find_comparable_products(
    category: str,
    complexity: str,
    material_cost: float,
    data_path: str = "data/cleaned_sales_data.csv",
    top_n: int = 5,
    cost_tolerance: float = 0.3,
) -> pd.DataFrame:
    """
    Returns the top_n most comparable historical products.

    Matching logic:
    1. Same category (required)
    2. Same complexity level (required)
    3. Material cost within +/- cost_tolerance (e.g. 30%) of the target
    4. Ranked by closeness of material cost
    """
    df = pd.read_csv(data_path)

    candidates = df[
        (df["category"] == category) & (df["complexity_level"] == complexity)
    ].copy()

    if candidates.empty:
        return pd.DataFrame()  # no comparable products found

    lower_bound = material_cost * (1 - cost_tolerance)
    upper_bound = material_cost * (1 + cost_tolerance)

    candidates = candidates[
        (candidates["material_cost"] >= lower_bound)
        & (candidates["material_cost"] <= upper_bound)
    ]

    if candidates.empty:
        # widen search: drop the cost filter, just use category + complexity
        candidates = df[
            (df["category"] == category) & (df["complexity_level"] == complexity)
        ].copy()

    candidates["cost_distance"] = (candidates["material_cost"] - material_cost).abs()
    candidates = candidates.sort_values("cost_distance").head(top_n)

    return candidates[["product_id", "category", "complexity_level",
                        "material_cost", "final_selling_price", "region", "season"]]


if __name__ == "__main__":
    # Example: a new saree with medium complexity, material cost 500
    results = find_comparable_products(
        category="sarees", complexity="medium", material_cost=500
    )
    print("Comparable products found:")
    print(results)

    if not results.empty:
        avg_price = results["final_selling_price"].mean()
        print(f"\nAverage selling price of comparable products: rupees {avg_price:.2f}")