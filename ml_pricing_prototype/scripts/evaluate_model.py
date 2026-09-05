"""
PROTOTYPE / FUTURE SCOPE ONLY - see generate_synthetic_dataset.py header.

Evaluates the trained model on the held-out test set (data it never saw
during training), giving an honest measure of real-world performance.
"""

import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error


def evaluate_model():
    model = joblib.load("models/pricing_model.pkl")
    X_test = pd.read_csv("data/X_test.csv")
    y_test = pd.read_csv("data/y_test.csv").squeeze()  # squeeze to a Series

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    mape = mean_absolute_percentage_error(y_test, predictions) * 100

    print("=" * 50)
    print("MODEL EVALUATION RESULTS")
    print("=" * 50)
    print(f"Mean Absolute Error (MAE):        rupees {mae:.2f}")
    print(f"Mean Absolute Percentage Error:   {mape:.2f}%")
    print(f"R-squared Score:                  {r2:.4f}")
    print("=" * 50)

    print("\nWhat this means in plain words:")
    print(f"- On average, predictions are off by about rupees {mae:.0f}")
    print(f"  ({mape:.1f}% of the actual price, on average)")
    print(f"- The model explains {r2*100:.1f}% of the price variation in the data")

    # Show a few example predictions vs actual, side by side
    comparison = pd.DataFrame({
        "actual_price": y_test.values[:10],
        "predicted_price": predictions[:10].round(2),
    })
    comparison["difference"] = (comparison["actual_price"] - comparison["predicted_price"]).round(2)
    print("\nSample predictions vs actual:")
    print(comparison)


if __name__ == "__main__":
    evaluate_model()