"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Transforms the cleaned dataset into a model-ready feature set:
- Encodes categorical columns (category, complexity, region, season) as numbers
- Merges in the seasonal trend multiplier calculated earlier
- Saves the final feature matrix + target column for training
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib


def build_features(
    data_path: str = "data/cleaned_sales_data.csv",
    trends_path: str = "data/price_trends.csv",
) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    trends = pd.read_csv(trends_path)

    # Merge in the seasonal trend multiplier we calculated in Step 8
    df = df.merge(trends, on=["category", "season"], how="left")

    # Base cost - a simple derived feature (material + labor)
    df["base_cost"] = df["material_cost"] + df["labor_cost"]

    # Encode categorical columns into numbers, saving each encoder so we can
    # reverse the encoding later (needed when the model is actually used)
    encoders = {}
    categorical_columns = ["category", "complexity_level", "region", "season"]

    for col in categorical_columns:
        encoder = LabelEncoder()
        df[f"{col}_encoded"] = encoder.fit_transform(df[col])
        encoders[col] = encoder

    joblib.dump(encoders, "models/label_encoders.pkl")
    print("Saved label encoders to: models/label_encoders.pkl")

    feature_columns = [
        "material_cost", "labor_cost", "base_cost", "trend_multiplier",
        "category_encoded", "complexity_level_encoded",
        "region_encoded", "season_encoded",
    ]
    target_column = "final_selling_price"

    final_df = df[feature_columns + [target_column]]
    final_df.to_csv("data/features_ready.csv", index=False)

    print(f"\nFeature matrix shape: {final_df.shape}")
    print(f"Saved to: data/features_ready.csv")
    print("\nSample rows:")
    print(final_df.head())

    return final_df


if __name__ == "__main__":
    build_features()