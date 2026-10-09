import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "data/online_retail_5000.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Original shape:", df.shape)


# ============================================================
# 2. BASIC INSPECTION
# ============================================================

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATES ---")
print("Duplicate rows:", df.duplicated().sum())


# ============================================================
# 3. REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates()

print("\nRemoved duplicates:", duplicate_count)
print("Shape after removing duplicates:", df.shape)


# ============================================================
# 4. HANDLE MISSING CUSTOMER IDs
# ============================================================

missing_customer_ids = df["CustomerID"].isnull().sum()

print("\nMissing Customer IDs:", missing_customer_ids)

# Since CustomerID is important for customer-level analysis,
# remove rows where CustomerID is missing.

df = df.dropna(subset=["CustomerID"])

print("Shape after removing missing Customer IDs:", df.shape)


# ============================================================
# 5. HANDLE MISSING DESCRIPTIONS
# ============================================================

missing_descriptions = df["Description"].isnull().sum()

print("\nMissing Descriptions:", missing_descriptions)

df = df.dropna(subset=["Description"])

print("Shape after removing missing Descriptions:", df.shape)


# ============================================================
# 6. CONVERT DATA TYPES
# ============================================================

df["CustomerID"] = df["CustomerID"].astype(int)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\nData types after conversion:")
print(df.dtypes)


# ============================================================
# 7. CHECK NEGATIVE VALUES
# ============================================================

negative_quantity = (df["Quantity"] < 0).sum()

negative_price = (df["UnitPrice"] < 0).sum()

print("\nNegative Quantity records:", negative_quantity)
print("Negative UnitPrice records:", negative_price)


# ============================================================
# 8. REMOVE INVALID SALES RECORDS
# ============================================================

# For our sales analysis, we only want actual positive sales.

df = df[df["Quantity"] > 0]

df = df[df["UnitPrice"] > 0]

print("\nShape after removing invalid sales:")
print(df.shape)


# ============================================================
# 9. CREATE TOTAL SALES COLUMN
# ============================================================

df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

print("\n--- SAMPLE WITH TOTAL AMOUNT ---")

print(
    df[
        [
            "InvoiceNo",
            "Description",
            "Quantity",
            "UnitPrice",
            "TotalAmount"
        ]
    ].head()
)


# ============================================================
# 10. FINAL DATASET SUMMARY
# ============================================================

print("\n====================================")
print("FINAL DATASET SUMMARY")
print("====================================")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("Unique Customers:", df["CustomerID"].nunique())

print("Unique Products:", df["Description"].nunique())

print("Unique Countries:", df["Country"].nunique())

print("Unique Orders:", df["InvoiceNo"].nunique())

print("Total Revenue:", round(df["TotalAmount"].sum(), 2))

# ============================================================
# 11. EXPLORATORY DATA ANALYSIS
# ============================================================

print("\n====================================")
print("EXPLORATORY DATA ANALYSIS")
print("====================================")


# ------------------------------------------------------------
# 11.1 TOTAL REVENUE
# ------------------------------------------------------------

total_revenue = df["TotalAmount"].sum()

print("\nTotal Revenue:")
print(round(total_revenue, 2))


# ------------------------------------------------------------
# 11.2 AVERAGE TRANSACTION VALUE
# ------------------------------------------------------------

average_transaction = df["TotalAmount"].mean()

print("\nAverage Transaction Value:")
print(round(average_transaction, 2))


# ------------------------------------------------------------
# 11.3 MEDIAN TRANSACTION VALUE
# ------------------------------------------------------------

median_transaction = df["TotalAmount"].median()

print("\nMedian Transaction Value:")
print(round(median_transaction, 2))


# ------------------------------------------------------------
# 11.4 TOTAL QUANTITY SOLD
# ------------------------------------------------------------

total_quantity = df["Quantity"].sum()

print("\nTotal Quantity Sold:")
print(total_quantity)


# ------------------------------------------------------------
# 11.5 TOP 10 PRODUCTS BY REVENUE
# ------------------------------------------------------------

top_products = (
    df.groupby("Description")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products)


# ------------------------------------------------------------
# 11.6 TOP 10 PRODUCTS BY QUANTITY
# ------------------------------------------------------------

top_products_quantity = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Quantity Sold:")
print(top_products_quantity)


# ------------------------------------------------------------
# 11.7 SALES BY COUNTRY
# ------------------------------------------------------------

country_sales = (
    df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Countries by Revenue:")
print(country_sales)


# ------------------------------------------------------------
# 11.8 CUSTOMER REVENUE
# ------------------------------------------------------------

customer_revenue = (
    df.groupby("CustomerID")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Revenue:")
print(customer_revenue)


# ------------------------------------------------------------
# 11.9 MONTHLY SALES
# ------------------------------------------------------------

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("YearMonth")["TotalAmount"]
    .sum()
)

print("\nMonthly Revenue:")
print(monthly_sales)


# ------------------------------------------------------------
# 11.10 SALES BY COUNTRY
# ------------------------------------------------------------

print("\nRevenue by Country:")
print(
    df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
)


# ------------------------------------------------------------
# 11.11 BASIC STATISTICS
# ------------------------------------------------------------

print("\n====================================")
print("STATISTICAL ANALYSIS")
print("====================================")

print("\nQuantity Statistics:")
print(df["Quantity"].describe())

print("\nUnit Price Statistics:")
print(df["UnitPrice"].describe())

print("\nTotal Amount Statistics:")
print(df["TotalAmount"].describe())


# ------------------------------------------------------------
# 11.12 CORRELATION
# ------------------------------------------------------------

correlation = df["Quantity"].corr(df["UnitPrice"])

print("\nCorrelation between Quantity and Unit Price:")
print(round(correlation, 4))

# ============================================================
# 12. OUTLIER ANALYSIS
# ============================================================

print("\n====================================")
print("OUTLIER ANALYSIS")
print("====================================")

# Function to calculate outliers using IQR
def find_outliers(column):

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    print(f"\n{column}")
    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)
    print("Number of Outliers:", len(outliers))

    return outliers


quantity_outliers = find_outliers("Quantity")
amount_outliers = find_outliers("TotalAmount")


print("\n--- TOP QUANTITY OUTLIERS ---")
print(
    quantity_outliers[
        ["Description", "Quantity", "UnitPrice", "TotalAmount"]
    ]
    .sort_values("Quantity", ascending=False)
    .head(10)
)


print("\n--- TOP REVENUE OUTLIERS ---")
print(
    amount_outliers[
        ["Description", "Quantity", "UnitPrice", "TotalAmount"]
    ]
    .sort_values("TotalAmount", ascending=False)
    .head(10)
)
# ============================================================
# SAVE CLEANED DATA FOR SQL
# ============================================================

cleaned_file = "data/cleaned_online_retail.csv"

df.to_csv(cleaned_file, index=False)

print("\nCleaned dataset saved successfully!")
print("File:", cleaned_file)