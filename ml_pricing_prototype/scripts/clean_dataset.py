"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Cleans the synthetic dataset: checks for missing values, duplicates,
and removes unrealistic outliers before it's used for analysis/training.
"""

import pandas as pd


def clean_dataset(input_path="data/synthetic_sales_data.csv",
                   output_path="data/cleaned_sales_data.csv"):
    df = pd.read_csv(input_path)

    print(f"Loaded {len(df)} rows")

    # 1. Check for missing values
    missing_counts = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_counts[missing_counts > 0] if missing_counts.sum() > 0 else "None found")
    df = df.dropna()

    # 2. Check for duplicate product_ids
    duplicate_count = df.duplicated(subset=["product_id"]).sum()
    print(f"\nDuplicate product_ids found: {duplicate_count}")
    df = df.drop_duplicates(subset=["product_id"])

    # 3. Remove unrealistic values (negative or zero costs/prices)
    before = len(df)
    df = df[(df["material_cost"] > 0) & (df["labor_cost"] > 0) & (df["final_selling_price"] > 0)]
    removed = before - len(df)
    print(f"Removed {removed} rows with non-positive cost/price values")

    # 4. Remove extreme outliers using the IQR method on final_selling_price
    q1 = df["final_selling_price"].quantile(0.25)
    q3 = df["final_selling_price"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    before = len(df)
    df = df[(df["final_selling_price"] >= lower_bound) & (df["final_selling_price"] <= upper_bound)]
    removed = before - len(df)
    print(f"Removed {removed} outlier rows outside [{lower_bound:.2f}, {upper_bound:.2f}]")

    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved: {len(df)} rows -> {output_path}")

    return df


if __name__ == "__main__":
    clean_dataset()