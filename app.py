
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Video Game Sales Analysis")
st.write("Explore video game sales across platforms, genres, publishers and regions.")

# Load Dataset
df = pd.read_csv("vgsales.csv")

# Data Cleaning
df.Year = df.Year.fillna(0)
df.Publisher = df.Publisher.fillna(0)

# Outlier Removal
i = 'Global_Sales'

q1 = np.percentile(df[i], 25)
q3 = np.percentile(df[i], 75)

iqr = q3 - q1

c1 = q1 - 1.5 * iqr
c2 = q3 + 1.5 * iqr

t = df[(df[i] > c2) | (df[i] < c1)]
t = t.index

df = df.drop(labels=t)

# Sidebar
st.sidebar.title("Dashboard Menu")

menu = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Platform Analysis",
        "Genre Analysis",
        "Yearly Trends",
        "Publisher Analysis",
        "Regional Sales",
        "Top 10 Games"
    ]
)

# Overview
if menu == "Overview":

    st.header("Sales Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Games", df.Name.nunique())
    col2.metric("Global Sales", round(df.Global_Sales.sum(), 2))
    col3.metric("Total Platforms", df.Platform.nunique())
    col4.metric("Total Publishers", df.Publisher.nunique())

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10))

    st.subheader("Dataset Description")
    st.dataframe(df.describe())

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum())

    st.subheader("Global Sales Distribution")

    fig, ax = plt.subplots()
    sb.histplot(df.Global_Sales, ax=ax)
    st.pyplot(fig)

    st.subheader("Global Sales Boxplot")

    fig, ax = plt.subplots()
    sb.boxplot(x=df.Global_Sales, ax=ax)
    st.pyplot(fig)


# Platform Analysis
elif menu == "Platform Analysis":

    st.header("Platform Analysis")

    platform_sales = df.groupby('Platform')['Global_Sales'].sum().reset_index()

    st.subheader("Platform vs Global Sales")

    fig, ax = plt.subplots(figsize=(12, 5))
    sb.barplot(data=platform_sales, x='Platform',
               y='Global_Sales', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Platform Sales Summary")

    st.dataframe(
        df.groupby('Platform')['Global_Sales'].agg(['sum', 'mean'])
    )


# Genre Analysis
elif menu == "Genre Analysis":

    st.header("Genre Analysis")

    genre_sales = df.groupby('Genre')['Global_Sales'].sum().reset_index()

    st.subheader("Genre vs Global Sales")

    fig, ax = plt.subplots(figsize=(10, 5))
    sb.barplot(data=genre_sales, x='Genre',
               y='Global_Sales', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Genre Sales Summary")

    st.dataframe(
        df.groupby('Genre')['Global_Sales'].agg(['sum', 'mean'])
    )

    st.subheader("North America Sales by Genre")

    st.dataframe(
        df.groupby('Genre')['NA_Sales'].agg(['sum', 'mean'])
    )


# Yearly Trends
elif menu == "Yearly Trends":

    st.header("Yearly Sales Trends")

    Trends = df.groupby(
        ['Year', 'Genre']
    )['Global_Sales'].sum().reset_index()

    Trends = Trends[Trends.Year != 0]

    fig, ax = plt.subplots(figsize=(12, 6))

    sb.lineplot(
        data=Trends,
        x='Year',
        y='Global_Sales',
        hue='Genre',
        ax=ax
    )

    plt.title("Sales Data by Year and Genre")
    st.pyplot(fig)

    st.subheader("Year and Platform Sales")

    st.dataframe(
        df.groupby(['Year', 'Platform'])['Global_Sales'].sum()
    )


# Publisher Analysis
elif menu == "Publisher Analysis":

    st.header("Publisher Analysis")

    top_performing = df.groupby(
        'Publisher'
    )['Global_Sales'].sum().nlargest(10).reset_index()

    st.subheader("Top 10 Performing Publishers")

    fig, ax = plt.subplots(figsize=(12, 5))

    sb.barplot(
        data=top_performing,
        x='Publisher',
        y='Global_Sales',
        ax=ax
    )

    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Publisher Regional Performance")

    Publisher_performance = df.groupby('Publisher')[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    ].sum()

    st.dataframe(Publisher_performance)


# Regional Sales
elif menu == "Regional Sales":

    st.header("Regional Sales Analysis")

    region_sales = df[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    ].sum()

    st.subheader("Sales by Region")

    fig, ax = plt.subplots()

    region_sales.plot(kind='bar', ax=ax)

    plt.ylabel("Sales")
    plt.xticks(rotation=0)
    st.pyplot(fig)

    st.subheader("Regional Sales Summary")
    st.dataframe(region_sales)

    st.subheader("Regional Sales Comparison")

    fig, ax = plt.subplots(figsize=(10, 5))

    sb.barplot(data=df[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
    ], ax=ax)

    st.pyplot(fig)


# Top 10 Games
elif menu == "Top 10 Games":

    st.header("Top 10 Games by Region")

    n = df.sort_values(
        by='NA_Sales', ascending=False
    ).head(10)

    e = df.sort_values(
        by='EU_Sales', ascending=False
    ).head(10)

    j = df.sort_values(
        by='JP_Sales', ascending=False
    ).head(10)

    o = df.sort_values(
        by='Other_Sales', ascending=False
    ).head(10)

    st.subheader("Top 10 Games - North America")

    fig, ax = plt.subplots(figsize=(12, 5))
    sb.barplot(data=n, x='Name', y='NA_Sales', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Top 10 Games - Europe")

    fig, ax = plt.subplots(figsize=(12, 5))
    sb.barplot(data=e, x='Name', y='EU_Sales', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Top 10 Games - Japan")

    fig, ax = plt.subplots(figsize=(12, 5))
    sb.barplot(data=j, x='Name', y='JP_Sales', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Top 10 Games - Other Regions")

    fig, ax = plt.subplots(figsize=(12, 5))
    sb.barplot(data=o, x='Name', y='Other_Sales', ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Top 10 Games Data")

    st.dataframe(n[['Name', 'Platform', 'NA_Sales']])
