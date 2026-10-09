
# E-Commerce Sales & Customer Analytics

## Project Overview

This project analyzes e-commerce transaction data to understand sales performance, customer spending, product revenue, and geographic trends.

It uses Python for data cleaning and exploratory data analysis, MySQL for querying business metrics, Streamlit for interactive visualization, and Scikit-learn to demonstrate monthly revenue prediction using Linear Regression.

## Objectives

- Clean and prepare raw transaction data.
- Explore sales, customer, and product performance.
- Analyze business metrics using SQL.
- Build an interactive dashboard.
- Demonstrate a basic machine learning workflow.
- Present findings that can support business decisions.

## Tech Stack

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- MySQL
- Streamlit
- Scikit-learn
- Git and GitHub

## Dataset

The project uses a sample of 5,000 transactions from the UCI Online Retail dataset.

After cleaning, 3,638 records remained for analysis.

The data includes invoice numbers, product codes, descriptions, quantities, invoice dates, unit prices, customer IDs, and countries.

A `TotalAmount` feature was created:

`TotalAmount = Quantity × UnitPrice`

The `YearMonth` field was also used for monthly analysis.

## Project Workflow

1. **Data preparation:** Sampled the original dataset and loaded it using Pandas.
2. **Data cleaning:** Handled missing customer IDs and descriptions, removed duplicate rows, filtered invalid sales records, and converted dates to datetime.
3. **Feature engineering:** Calculated transaction amounts and extracted monthly information.
4. **Exploratory Data Analysis:** Analyzed revenue, products, customers, countries, monthly trends, summary statistics, and outliers.
5. **SQL analysis:** Used MySQL to calculate revenue, order counts, customer spending, top products, and country-wise sales.
6. **Dashboard:** Built a Streamlit dashboard with metrics, filters, charts, and business insights.
7. **Machine learning:** Trained a Linear Regression model using monthly revenue and a time index, then evaluated its predictions on later months.

## Key Findings

- The cleaned sample contains 3,638 transaction records.
- The sample includes 1,729 unique customers and 1,575 unique products.
- Total revenue in the cleaned sample is 77,493.36 dataset currency units.
- The United Kingdom generated the largest share of sample revenue.
- The highest-revenue product and the highest-quantity product were different.
- Monthly revenue varied considerably across the observed period.

These findings describe the sampled records and should not be treated as estimates of the retailer's full business performance.

## Machine Learning Results

The model uses Linear Regression to estimate monthly revenue from a sequential month index.

Evaluation on the final three months of the observed series:

- Mean Absolute Error (MAE): 3672.78
- Root Mean Squared Error (RMSE): 3841.57
- R-squared (R²): -0.137

The negative R² indicates that this model performed worse than a baseline that predicts the average revenue of the test period.

The model is included to demonstrate the ML workflow, not as a reliable forecasting solution. The random transaction sample and simple time-only feature limit its predictive value.

## Project Structure

```text
E-Commerce-Sales-Analytics/
├── data/
│   ├── online_retail_5000.csv
│   ├── cleaned_online_retail.csv
│   └── monthly_sales.csv
├── src/
│   ├── analysis.py
│   └── sales_prediction.py
├── sql/
│   └── analysis.sql
├── dashboard.py
├── create_dataset.py
├── import_to_mysql.py
├── monthly_sales_prediction.png
└── README.md
```

## How to Run

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install pandas numpy matplotlib seaborn scikit-learn streamlit openpyxl mysql-connector-python
```

### 3. Run the Streamlit dashboard

```powershell
streamlit run dashboard.py
```

### 4. Run the sales prediction model

```powershell
python src/sales_prediction.py
```

### 5. Import data into MySQL

Configure your local MySQL connection and database, then run:

```powershell
python import_to_mysql.py
```

The database and table must exist before running the import script.

## Future Improvements

- Use the complete dataset and validate results on representative data.
- Improve forecasting with seasonal features and suitable time-series models.
- Compare against a baseline forecast.
- Add automated tests and stronger data validation.
- Improve dashboard deployment and documentation.

## Author

Developed as a data analytics and machine learning portfolio project.
