
import pandas as pd
import mysql.connector
from getpass import getpass

# ============================================================
# 1. LOAD THE CLEANED CSV
# ============================================================

CSV_PATH = "data/cleaned_online_retail.csv"

df = pd.read_csv(CSV_PATH)

print("Original CSV columns:", df.columns.tolist())
print("Original CSV rows:", len(df))

# ============================================================
# 2. KEEP ONLY THE NINE MYSQL TABLE COLUMNS
# YearMonth is excluded because it is not in the SQL table.
# ============================================================

mysql_columns = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
    "TotalAmount"
]

missing_columns = [
    col for col in mysql_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Required CSV columns are missing: {missing_columns}")

df = df[mysql_columns].copy()

# ============================================================
# 3. CLEAN VALUES FOR MYSQL
# ============================================================

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

# Convert pandas missing values to Python None (SQL NULL)
df = df.astype(object).where(pd.notna(df), None)

# Prepare records for insertion
records = []

for row in df.itertuples(index=False, name=None):
    values = list(row)

    # Convert InvoiceDate to a Python datetime object
    if values[4] is not None:
        values[4] = pd.Timestamp(values[4]).to_pydatetime()

    records.append(tuple(values))

print("Columns per record:", len(records[0]) if records else 0)
print("Records prepared:", len(records))

if records and len(records[0]) != 9:
    raise ValueError("Each record must contain exactly 9 values.")

# ============================================================
# 4. CONNECT TO MYSQL
# ============================================================

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=getpass("Enter your MySQL root password: "),
        database="analytics"
    )

    cursor = connection.cursor()
    print("\nConnected to MySQL successfully!")

    # ========================================================
    # 5. VERIFY THE TABLE STRUCTURE
    # ========================================================

    cursor.execute("DESCRIBE cleaned_online_retail")
    table_columns = cursor.fetchall()

    print("MySQL table columns:", len(table_columns))

    if len(table_columns) != 9:
        raise ValueError(
            "Expected 9 columns in cleaned_online_retail. "
            f"Found {len(table_columns)}."
        )

    # ========================================================
    # 6. INSERT DATA IN BATCHES
    # ========================================================

    insert_sql = """
        INSERT INTO cleaned_online_retail
        (
            InvoiceNo,
            StockCode,
            Description,
            Quantity,
            InvoiceDate,
            UnitPrice,
            CustomerID,
            Country,
            TotalAmount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print("SQL placeholders:", insert_sql.count("%s"))

    # Replace existing data so rerunning doesn't duplicate rows.
    # The transaction is rolled back if insertion fails.
    try:
        cursor.execute("START TRANSACTION")
        cursor.execute("DELETE FROM cleaned_online_retail")

        batch_size = 500

        for start in range(0, len(records), batch_size):
            batch = records[start:start + batch_size]

            cursor.executemany(insert_sql, batch)

            print(
                f"Inserted {min(start + batch_size, len(records))}"
                f" / {len(records)} rows"
            )

        # Verify before committing
        cursor.execute("SELECT COUNT(*) FROM cleaned_online_retail")
        total_rows = cursor.fetchone()[0]

        if total_rows != len(records):
            raise ValueError(
                f"Row count mismatch: expected {len(records)}, "
                f"found {total_rows}."
            )

        connection.commit()

        print("\n===================================")
        print("IMPORT COMPLETED SUCCESSFULLY!")
        print("Expected rows:", len(records))
        print("Rows in MySQL:", total_rows)
        print("Database: analytics")
        print("Table: cleaned_online_retail")
        print("===================================")

    except Exception:
        connection.rollback()
        raise

except Exception as error:
    print("\nImport failed:", repr(error))

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
