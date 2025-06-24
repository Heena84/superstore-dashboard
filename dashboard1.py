import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- Title ---
st.set_page_config(page_title="Superstore Dashboard", layout="wide")
st.title("🛍️ Superstore Sales Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    df=pd.read_csv("Data/sales_data.csv",encoding='ISO-8859-1')
    df.columns = df.columns.str.strip()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("📊 Filter Data")

# Region Filter
region = st.sidebar.multiselect(
    "Select Region", options=df["Region"].dropna().unique(),
    default=df["Region"].dropna().unique()
)

# Category Filter
category = st.sidebar.multiselect(
    "Select Category", options=df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

# Sub-Category Filter
subcategory = st.sidebar.multiselect(
    "Select Sub-Category", options=df["Sub-Category"].dropna().unique(),
    default=df["Sub-Category"].dropna().unique()
)

# Date Range Filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# --- Apply Filters ---
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(subcategory)) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# --- KPIs ---
st.subheader("📌 Key Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")

# --- Monthly Sales Trend ---
st.subheader("📈 Monthly Sales Trend")
monthly_sales = (
    filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .sort_index()
)
monthly_sales.index = monthly_sales.index.astype(str)

fig, ax = plt.subplots(figsize=(10, 4))
monthly_sales.plot(kind="bar", ax=ax, color="skyblue")
ax.set_ylabel("Sales")
ax.set_xlabel("Month")
ax.set_title("Sales by Month")
st.pyplot(fig)

# --- Raw Data Option ---
with st.expander("🗂 Show Filtered Data Table"):
    st.dataframe(filtered_df)

# --- Download Button ---
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Filtered Data as CSV",
    csv,
    "filtered_sales_data.csv",
    "text/csv",
    help="Download current view as CSV"
)
