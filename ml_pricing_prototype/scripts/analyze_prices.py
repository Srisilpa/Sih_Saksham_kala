"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Analyzes historical price patterns in the cleaned dataset:
average price per category, price ranges, and seasonal effects.
"""

import pandas as pd


def analyze_prices(input_path="data/cleaned_sales_data.csv"):
    df = pd.read_csv(input_path)

    print("=" * 60)
    print("PRICE ANALYSIS BY CATEGORY")
    print("=" * 60)
    category_stats = df.groupby("category")["final_selling_price"].agg(
        ["mean", "median", "min", "max", "count"]
    ).round(2)
    category_stats = category_stats.sort_values("mean", ascending=False)
    print(category_stats)

    print("\n" + "=" * 60)
    print("PRICE ANALYSIS BY COMPLEXITY LEVEL")
    print("=" * 60)
    complexity_stats = df.groupby("complexity_level")["final_selling_price"].agg(
        ["mean", "median", "count"]
    ).round(2)
    print(complexity_stats)

    print("\n" + "=" * 60)
    print("PRICE ANALYSIS BY SEASON")
    print("=" * 60)
    season_stats = df.groupby("season")["final_selling_price"].agg(
        ["mean", "median", "count"]
    ).round(2)
    print(season_stats)

    print("\n" + "=" * 60)
    print("PRICE ANALYSIS BY REGION")
    print("=" * 60)
    region_stats = df.groupby("region")["final_selling_price"].agg(
        ["mean", "median", "count"]
    ).round(2)
    print(region_stats)

    # Save a summary report to file too, useful for including in your report/slides
    with open("data/price_analysis_summary.txt", "w") as f:
        f.write("PRICE ANALYSIS SUMMARY (synthetic prototype data)\n\n")
        f.write("By Category:\n")
        f.write(category_stats.to_string())
        f.write("\n\nBy Complexity:\n")
        f.write(complexity_stats.to_string())
        f.write("\n\nBy Season:\n")
        f.write(season_stats.to_string())
        f.write("\n\nBy Region:\n")
        f.write(region_stats.to_string())

    print("\nSummary saved to: data/price_analysis_summary.txt")


if __name__ == "__main__":
    analyze_prices()
