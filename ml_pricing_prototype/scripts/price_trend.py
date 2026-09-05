"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Calculates price trend multipliers per season and category, based on
historical data. These trend multipliers can be used as a feature for
the ML model, or directly as a business rule adjustment.
"""

import pandas as pd


def calculate_price_trends(data_path: str = "data/cleaned_sales_data.csv") -> pd.DataFrame:
    """
    For each category, calculates how much higher/lower prices tend to be
    in each season compared to that category's overall average.

    Returns a DataFrame with a 'trend_multiplier' column:
    - 1.0 means "no change from average"
    - 1.15 means "15% higher than average in this season"
    - 0.90 means "10% lower than average in this season"
    """
    df = pd.read_csv(data_path)

    category_avg = df.groupby("category")["final_selling_price"].mean().rename("category_avg_price")
    df = df.merge(category_avg, on="category")

    season_category_avg = (
        df.groupby(["category", "season"])["final_selling_price"]
        .mean()
        .reset_index()
        .rename(columns={"final_selling_price": "season_avg_price"})
    )

    season_category_avg = season_category_avg.merge(
        category_avg.reset_index(), on="category"
    )

    season_category_avg["trend_multiplier"] = (
        season_category_avg["season_avg_price"] / season_category_avg["category_avg_price"]
    ).round(3)

    result = season_category_avg[["category", "season", "trend_multiplier"]]
    result = result.sort_values(["category", "season"])

    result.to_csv("data/price_trends.csv", index=False)
    print("Price trend multipliers saved to: data/price_trends.csv\n")
    print(result.to_string(index=False))

    return result


if __name__ == "__main__":
    calculate_price_trends()