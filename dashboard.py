import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Main title */
.dashboard-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

/* Subtitle */
.dashboard-subtitle {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 25px;
}

/* Metric cards */
.metric-card {
    background-color: #161a23;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2a2f3a;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #9ca3af;
}

.metric-value {
    font-size: 25px;
    font-weight: 700;
    margin-top: 5px;
}

/* Section headings */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 12px;
}

/* Business insight cards */
.insight-box {
    background-color: #161a23;
    color: #f3f4f6;
    padding: 18px 20px;
    border-radius: 12px;
    border: 1px solid #2a2f3a;
    margin-bottom: 12px;
    font-size: 15px;
    line-height: 1.6;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/online_retail_5000.csv"
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove missing CustomerID
    df = df.dropna(
        subset=["CustomerID"]
    )

    # Remove missing descriptions
    df = df.dropna(
        subset=["Description"]
    )

    # Convert CustomerID
    df["CustomerID"] = (
        df["CustomerID"]
        .astype(int)
    )

    # Convert date
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    # Keep only valid sales
    df = df[
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ]

    # Calculate revenue
    df["TotalAmount"] = (
        df["Quantity"] *
        df["UnitPrice"]
    )

    return df


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🛒 E-Commerce Sales Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive dashboard for exploring sales, '
    'customers, products and revenue trends'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔍 Filters")

st.sidebar.markdown("### Country")

countries = sorted(
    df["Country"].unique()
)

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=[]
)

st.sidebar.markdown("### Date Range")

min_date = (
    df["InvoiceDate"]
    .min()
    .date()
)

max_date = (
    df["InvoiceDate"]
    .max()
    .date()
)

date_range = st.sidebar.date_input(
    "Select dates",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# Country filter
if selected_country:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(
            selected_country
        )
    ]


# Date filter
if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = (
        pd.Timestamp(date_range[1])
        + pd.Timedelta(days=1)
    )

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"] >= start_date)
        &
        (filtered_df["InvoiceDate"] < end_date)
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = (
    filtered_df["TotalAmount"].sum()
)

total_orders = (
    filtered_df["InvoiceNo"].nunique()
)

total_customers = (
    filtered_df["CustomerID"].nunique()
)

total_products = (
    filtered_df["StockCode"].nunique()
)

if total_orders > 0:

    order_values = (
        filtered_df
        .groupby("InvoiceNo")["TotalAmount"]
        .sum()
    )

    average_order_value = (
        order_values.mean()
    )

else:

    average_order_value = 0


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                💰 Total Revenue
            </div>
            <div class="metric-value">
                ₹{total_revenue:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🧾 Orders
            </div>
            <div class="metric-value">
                {total_orders:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                👥 Customers
            </div>
            <div class="metric-value">
                {total_customers:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                📦 Products
            </div>
            <div class="metric-value">
                {total_products:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                🛍️ Avg Order Value
            </div>
            <div class="metric-value">
                ₹{average_order_value:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# REVENUE TREND
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Monthly Revenue Trend'
    '</div>',
    unsafe_allow_html=True
)

if len(filtered_df) > 0:

    filtered_df["YearMonth"] = (
        filtered_df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_revenue = (
        filtered_df
        .groupby("YearMonth")["TotalAmount"]
        .sum()
    )

    st.line_chart(
        monthly_revenue
    )


# ============================================================
# TOP PRODUCTS + COUNTRY
# ============================================================

left_column, right_column = st.columns(2)


# ------------------------------------------------------------
# TOP PRODUCTS
# ------------------------------------------------------------

with left_column:

    st.markdown(
        '<div class="section-title">'
        '🏆 Top 10 Products by Revenue'
        '</div>',
        unsafe_allow_html=True
    )

    top_products = (
        filtered_df
        .groupby("Description")["TotalAmount"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
    )

    st.bar_chart(
        top_products
    )


# ------------------------------------------------------------
# COUNTRY REVENUE
# ------------------------------------------------------------

with right_column:

    st.markdown(
        '<div class="section-title">'
        '🌍 Top 10 Countries by Revenue'
        '</div>',
        unsafe_allow_html=True
    )

    country_revenue = (
        filtered_df
        .groupby("Country")["TotalAmount"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
    )

    st.bar_chart(
        country_revenue
    )


# ============================================================
# TOP CUSTOMERS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '👥 Top 10 Customers by Revenue'
    '</div>',
    unsafe_allow_html=True
)

customer_revenue = (
    filtered_df
    .groupby("CustomerID")["TotalAmount"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
)

st.bar_chart(
    customer_revenue
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Business Insights'
    '</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    # Highest revenue country
    country_sales = (
        filtered_df
        .groupby("Country")["TotalAmount"]
        .sum()
    )

    highest_country = (
        country_sales.idxmax()
    )

    highest_country_revenue = (
        country_sales.max()
    )


    # Highest revenue month
    filtered_df["YearMonth"] = (
        filtered_df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    month_sales = (
        filtered_df
        .groupby("YearMonth")["TotalAmount"]
        .sum()
    )

    highest_month = (
        month_sales.idxmax()
    )

    highest_month_revenue = (
        month_sales.max()
    )


    # Mean and median
    mean_transaction = (
        filtered_df["TotalAmount"]
        .mean()
    )

    median_transaction = (
        filtered_df["TotalAmount"]
        .median()
    )


    # Top customer
    customer_sales = (
        filtered_df
        .groupby("CustomerID")["TotalAmount"]
        .sum()
    )

    top_customer = (
        customer_sales.idxmax()
    )

    top_customer_revenue = (
        customer_sales.max()
    )


    # Top product
    product_sales = (
        filtered_df
        .groupby("Description")["TotalAmount"]
        .sum()
    )

    top_product = (
        product_sales.idxmax()
    )

    top_product_revenue = (
        product_sales.max()
    )


    # Insights
    insights = [

        f"🌍 **{highest_country}** generated the highest revenue "
        f"with **₹{highest_country_revenue:,.2f}**.",

        f"📅 **{highest_month}** recorded the highest monthly "
        f"revenue with **₹{highest_month_revenue:,.2f}**.",

        f"🏆 **{top_product}** was the highest-revenue product "
        f"with **₹{top_product_revenue:,.2f}**.",

        f"👤 Customer **{top_customer}** generated the highest "
        f"customer revenue of **₹{top_customer_revenue:,.2f}**.",

        f"📊 The average transaction value was "
        f"**₹{mean_transaction:,.2f}**, while the median was "
        f"**₹{median_transaction:,.2f}**. "
        f"The higher mean suggests that some high-value "
        f"transactions are increasing the average."

    ]


    for insight in insights:

        st.markdown(
            f"""
            <div class="insight-box">
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📋 Data Explorer'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore the transactions after applying the selected filters."
)


display_columns = [

    "InvoiceNo",

    "InvoiceDate",

    "Description",

    "Quantity",

    "UnitPrice",

    "TotalAmount",

    "CustomerID",

    "Country"

]


st.dataframe(
    filtered_df[
        display_columns
    ].head(200),

    use_container_width=True,

    height=400
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'E-Commerce Sales Analytics • '
    'Python • Pandas • NumPy • Streamlit'
    '</div>',
    unsafe_allow_html=True
)