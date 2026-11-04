
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Fashion Trends Analysis",
    page_icon="👗",
    layout="wide"
)

# Title
st.title("👗 Fashion Trends Analysis Dashboard")
st.write("Explore fashion brands, categories, prices and discounts.")

# Upload Dataset
st.sidebar.header("Upload Dataset")

file = st.sidebar.file_uploader("Upload Fashion Trends CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
else:
    try:
        df = pd.read_csv("Fashion_Trends.csv")
    except FileNotFoundError:
        st.warning("Please upload Fashion_Trends.csv to continue.")
        st.stop()

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Home",
        "Data Overview",
        "Price Analysis",
        "Brand & Category Analysis",
        "Gender Analysis",
        "Discount Analysis",
        "Advanced Analysis"
    ]
)

# Home Dashboard
if menu == "Home":

    st.subheader("Fashion Trends Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Products", df.shape[0])
    col2.metric("Total Brands", df.Brand.nunique())
    col3.metric("Total Categories", df.Category.nunique())
    col4.metric("Average Discount", 
                round(df.Discount_Percentage.mean(), 2))

    st.divider()

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Missing Values")
        st.dataframe(df.isnull().sum())

    with col2:
        st.write("Data Types")
        st.dataframe(df.dtypes.astype(str))

# Data Overview
elif menu == "Data Overview":

    st.subheader("Dataset Overview")

    st.write("Dataset Shape:", df.shape)

    st.write("Column Names")
    st.write(df.columns.tolist())

    st.subheader("First 10 Records")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum())

    st.subheader("Data Types")
    st.dataframe(df.dtypes.astype(str))

    st.write("Total Records:", df.value_counts().sum())

# Price Analysis
elif menu == "Price Analysis":

    st.subheader("Price Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Original Price Distribution")
        fig, ax = plt.subplots()
        sb.histplot(df.Original_Price, ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.write("Discount Price Distribution")
        fig, ax = plt.subplots()
        sb.histplot(df.Discount_Price, ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Discount Percentage Distribution")

    fig, ax = plt.subplots()
    sb.histplot(df.Discount_Percentage, ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Discount Price Boxplot")

    fig, ax = plt.subplots()
    sb.boxplot(x=df.Discount_Price, ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Original Price Boxplot")

    fig, ax = plt.subplots()
    sb.boxplot(x=df.Original_Price, ax=ax)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Price vs Discount Analysis")

    fig, ax = plt.subplots()
    sb.scatterplot(
        x=df.Original_Price,
        y=df.Discount_Tier,
        ax=ax
    )
    ax.set_title("Price VS Discount Analysis")
    st.pyplot(fig)
    plt.close(fig)

# Brand and Category Analysis
elif menu == "Brand & Category Analysis":

    st.subheader("Top 10 Brands")

    b = df.Brand.value_counts().nlargest(10)

    fig, ax = plt.subplots()
    sb.barplot(x=b.index, y=b.values, ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel("Brand")
    ax.set_ylabel("Product Count")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Category Analysis")

    c = df.Category.value_counts()

    fig, ax = plt.subplots()
    sb.barplot(x=c.index, y=c.values, ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel("Category")
    ax.set_ylabel("Product Count")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Top 10 Categories")

    category = df.groupby("Category")["Product_Name"].count()
    category = category.sort_values(ascending=False).head(10)

    st.dataframe(category)

    st.subheader("Brand Product Count")
    st.dataframe(b)

# Gender Analysis
elif menu == "Gender Analysis":

    st.subheader("Gender-wise Product Analysis")

    g = df.groupby("Gender")["Product_Name"].count()

    fig, ax = plt.subplots()
    sb.barplot(x=g.index, y=g.values, ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel("Gender")
    ax.set_ylabel("Product Count")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Gender-wise Category Count")

    st.dataframe(
        df.groupby("Gender")["Category"].count()
    )

    st.subheader("Average Discount by Gender")

    st.dataframe(
        df.groupby("Gender")["Discount_Percentage"].mean()
    )

    st.subheader("Gender vs Discount Percentage")

    fig, ax = plt.subplots()
    sb.boxplot(
        x=df.Gender,
        y=df.Discount_Percentage,
        ax=ax
    )
    st.pyplot(fig)
    plt.close(fig)

# Discount Analysis
elif menu == "Discount Analysis":

    st.subheader("Discount Tier Analysis")

    st.dataframe(df.groupby("Discount_Tier").count())

    st.subheader("Average Discount by Product")

    st.dataframe(
        df.groupby("Product_Name")["Discount_Percentage"].mean()
    )

    st.subheader("Discount Tier vs Category")

    pt = pd.pivot_table(
        df,
        index="Category",
        columns="Discount_Tier",
        values="Product_ID",
        aggfunc="count",
        fill_value=0,
        margins=True
    )

    st.dataframe(pt, use_container_width=True)

    p = pd.crosstab(
        index=df.Discount_Tier,
        columns=df.Category,
        margins=True
    )

    st.write("Cross Tabulation")
    st.dataframe(p, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sb.heatmap(p, annot=True, fmt="g", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

# Advanced Analysis
elif menu == "Advanced Analysis":

    st.subheader("Price Segment Analysis")

    st.dataframe(df.Price_Segment.value_counts())

    st.subheader("Category vs Price Segment")

    ct = pd.crosstab(
        index=df.Category,
        columns=df.Price_Segment,
        margins=True
    )

    st.dataframe(ct, use_container_width=True)

    st.subheader("Brand vs Price Segment")

    pivot = pd.pivot_table(
        df,
        index="Brand",
        columns="Price_Segment",
        values="Original_Price",
        aggfunc="mean"
    )

    st.dataframe(pivot, use_container_width=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    sb.heatmap(pivot, annot=True, fmt=".0f", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Category-wise Product Count")

    st.dataframe(
        df.groupby("Price_Segment")["Category"].count()
    )

    st.subheader("Maximum Products by Name")

    st.write(df.Product_Name.value_counts().max())

# Footer
st.sidebar.divider()
st.sidebar.caption("Fashion Trends Analysis | Python Project")
