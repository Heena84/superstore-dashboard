import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Load data
df=pd.read_csv("data/sales_data.csv", encoding='ISO-8859-1')

# Clean column name in case it has leading/trailing spaces
df.columns = df.columns.str.strip()

# Convert Order Date safely
df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')

#Sidebar Filters
st.sidebar.title("Filters")
region = st.sidebar.selectbox("Select Region", df["Region"].unique())
category = st.sidebar.selectbox("Select Category", df["Category"].unique())

# Filtered data
filtered_df = df[(df["Region"] == region) & (df["Category"] == category)]

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
