import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Adidas Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Adidas US Sales Dashboard")
st.write("Analyze Adidas sales, products, regions, and profits.")

uploaded_file = st.file_uploader(
    "Upload your cleaned Adidas sales Excel file",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    required_columns = [
        "Product", "Region", "Total Sales",
        "Operating Profit", "Invoice Date"
    ]

    if all(col in df.columns for col in required_columns):
        df["Total Sales"] = pd.to_numeric(
            df["Total Sales"], errors="coerce"
        )
        df["Operating Profit"] = pd.to_numeric(
            df["Operating Profit"], errors="coerce"
        )
        df["Invoice Date"] = pd.to_datetime(
            df["Invoice Date"], errors="coerce"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Sales",
            f"${df['Total Sales'].sum():,.0f}"
        )
        col2.metric(
            "Operating Profit",
            f"${df['Operating Profit'].sum():,.0f}"
        )
        col3.metric(
            "Total Records",
            f"{len(df):,}"
        )

        st.subheader("Sales by Product")
        product_sales = df.groupby("Product")["Total Sales"].sum()
        st.bar_chart(product_sales)

        st.subheader("Sales by Region")
        region_sales = df.groupby("Region")["Total Sales"].sum()
        st.bar_chart(region_sales)

        st.subheader("Monthly Sales Trend")
        monthly_sales = (
            df.dropna(subset=["Invoice Date"])
              .assign(Month=lambda x: x["Invoice Date"].dt.to_period("M").astype(str))
              .groupby("Month")["Total Sales"].sum()
        )
        st.line_chart(monthly_sales)

        st.subheader("Operating Profit by Product")
        profit = df.groupby("Product")["Operating Profit"].sum()
        st.bar_chart(profit)

        st.subheader("Sales Data Preview")
        st.dataframe(df.head(100))

        st.download_button(
            "Download Cleaned Data",
            df.to_csv(index=False).encode("utf-8"),
            "Adidas_Cleaned_Sales.csv",
            "text/csv"
        )
    else:
        st.error(
            "The uploaded file is missing one or more required columns."
        )
else:
    st.info("Upload Adidas_Cleaned_Sales.xlsx to view the dashboard.")
