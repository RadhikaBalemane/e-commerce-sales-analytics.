
import pandas as pd
import numpy as np
import matplotlib

# Use a non-interactive backend to avoid the Tkinter error
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "cleaned_online_retail.csv"
MONTHLY_OUTPUT = PROJECT_ROOT / "data" / "monthly_sales.csv"
CHART_OUTPUT = PROJECT_ROOT / "monthly_sales_prediction.png"

# ============================================================
# 2. LOAD THE CLEANED DATA
# ============================================================

print("=" * 55)
print("E-COMMERCE MONTHLY SALES PREDICTION")
print("=" * 55)

df = pd.read_csv(DATA_PATH)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["TotalAmount"] = pd.to_numeric(
    df["TotalAmount"], errors="coerce"
)

df = df.dropna(subset=["InvoiceDate", "TotalAmount"])

print("\nDataset loaded successfully!")
print("Transaction rows:", len(df))

# ============================================================
# 3. AGGREGATE DATA BY MONTH
# ============================================================

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("YearMonth")["TotalAmount"]
    .sum()
    .sort_index()
    .reset_index()
)

monthly_sales["YearMonth"] = monthly_sales["YearMonth"].astype(str)
monthly_sales["MonthIndex"] = np.arange(len(monthly_sales))

print("\nMonthly Revenue:")
print(
    monthly_sales[["YearMonth", "TotalAmount"]]
    .to_string(index=False)
)

# Save monthly data
monthly_sales.to_csv(MONTHLY_OUTPUT, index=False)
print(f"\nMonthly sales saved to: {MONTHLY_OUTPUT}")

# ============================================================
# 4. PREPARE FEATURES AND TARGET
# ============================================================

X = monthly_sales[["MonthIndex"]]
y = monthly_sales["TotalAmount"]

if len(monthly_sales) < 5:
    raise ValueError(
        "At least 5 months of data are required for this demonstration."
    )

# Keep the later months for testing
split_index = max(1, int(len(monthly_sales) * 0.8))

if split_index >= len(monthly_sales):
    split_index = len(monthly_sales) - 1

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining months:", len(X_train))
print("Testing months:", len(X_test))

# ============================================================
# 5. TRAIN THE LINEAR REGRESSION MODEL
# ============================================================

model = LinearRegression()
model.fit(X_train, y_train)

print("\nLinear Regression model trained successfully!")

# ============================================================
# 6. EVALUATE THE MODEL
# ============================================================

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nMODEL EVALUATION")
print("-" * 35)
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

if len(y_test) >= 2:
    r2 = r2_score(y_test, y_pred)
    print(f"R-squared (R²): {r2:.3f}")
else:
    print("R-squared omitted: fewer than 2 test observations.")

# ============================================================
# 7. PREDICT THE NEXT MONTH
# ============================================================

next_month_index = len(monthly_sales)

next_month_revenue = model.predict(
    pd.DataFrame({"MonthIndex": [next_month_index]})
)[0]

last_month = pd.Period(
    monthly_sales["YearMonth"].iloc[-1], freq="M"
)
next_month = last_month + 1

print("\nNEXT MONTH PREDICTION")
print("-" * 35)
print("Prediction month:", next_month)
print(f"Predicted revenue: {next_month_revenue:.2f}")

# ============================================================
# 8. CREATE AND SAVE THE CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"],
    monthly_sales["TotalAmount"],
    marker="o",
    label="Actual Monthly Revenue"
)

plt.plot(
    monthly_sales["YearMonth"].iloc[split_index:],
    y_pred,
    marker="x",
    linestyle="--",
    label="Predicted Test Revenue"
)

plt.scatter(
    [str(next_month)],
    [next_month_revenue],
    marker="*",
    s=200,
    label="Next Month Prediction"
)

plt.title("Monthly Sales Revenue Prediction")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(CHART_OUTPUT, dpi=150, bbox_inches="tight")
plt.close()

print(f"\nPrediction chart saved to: {CHART_OUTPUT}")

# ============================================================
# 9. FINISH
# ============================================================

print("\n" + "=" * 55)
print("SALES PREDICTION SCRIPT COMPLETED SUCCESSFULLY")
print("=" * 55)
print("Output 1: data/monthly_sales.csv")
print("Output 2: monthly_sales_prediction.png")
