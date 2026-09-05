"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Trains a Random Forest Regressor to predict final_selling_price from
the engineered features. Splits data into train/test sets so we can
honestly evaluate performance on unseen data in the next step.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib


def train_model(data_path: str = "data/features_ready.csv"):
    df = pd.read_csv(data_path)

    feature_columns = [
        "material_cost", "labor_cost", "base_cost", "trend_multiplier",
        "category_encoded", "complexity_level_encoded",
        "region_encoded", "season_encoded",
    ]
    target_column = "final_selling_price"

    X = df[feature_columns]
    y = df[target_column]

    # 80% train, 20% test - the test set is never shown to the model during
    # training, so we can honestly measure how well it generalizes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training rows: {len(X_train)}, Test rows: {len(X_test)}")

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
    )

    model.fit(X_train, y_train)

    # Save everything needed for evaluation in the next step
    joblib.dump(model, "models/pricing_model.pkl")
    X_test.to_csv("data/X_test.csv", index=False)
    y_test.to_csv("data/y_test.csv", index=False)

    print("Model trained and saved to: models/pricing_model.pkl")

    # Show feature importance - which factors matter most to the model
    importance = pd.Series(model.feature_importances_, index=feature_columns)
    importance = importance.sort_values(ascending=False)
    print("\nFeature importance (which factors matter most):")
    print(importance.round(3))


if __name__ == "__main__":
    train_model()