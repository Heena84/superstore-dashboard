import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Load data
df=pd.read_csv("Data/sales_data.csv",encoding='ISO-8859-1')

#url = "https://raw.githubusercontent.com/ybifoundation/Dataset/main/Superstore.csv"
#df = pd.read_csv("https://raw.githubusercontent.com/ybifoundation/Dataset/main/Superstore.csv",encoding='ISO-8859-1')

# Clean column name in case it has leading/trailing spaces
df.columns = df.columns.str.strip()

# Convert Order Date safely
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')

# Sidebar filters
st.sidebar.header("📊 Filters")

# Region
region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())

# Category
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

# Sub-Category
subcategory = st.sidebar.multiselect("Select Sub-Category", options=df["Sub-Category"].unique(), default=df["Sub-Category"].unique())

# Date range
min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter dataset
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(subcategory)) &
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# Title and KPIs
st.title("📊 Superstore Sales Dashboard")
st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")

# Monthly trend
st.subheader("📈 Monthly Sales Trend")
monthly_sales = filtered_df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.astype(str)

fig, ax = plt.subplots()
monthly_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Sales")
st.pyplot(fig)

# Show data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
