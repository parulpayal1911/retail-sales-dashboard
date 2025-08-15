
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Retail Sales Performance Dashboard", layout="wide")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["order_date"])
    # Derived columns
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.month_name()
    df["aov"] = df["sales"]  # per order row; true AOV computed later
    return df

df = load_data("retail_sales.csv")

st.title("🛒 Retail Sales Performance Dashboard")

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filters")
min_date, max_date = df["order_date"].min(), df["order_date"].max()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
payments = st.sidebar.multiselect("Payment Method", sorted(df["payment_method"].unique()), default=sorted(df["payment_method"].unique()))

# Apply filters
mask = (
    (df["order_date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
    (df["region"].isin(regions)) &
    (df["category"].isin(categories)) &
    (df["payment_method"].isin(payments))
)
fdf = df.loc[mask].copy()

# ---- KPIs ----
total_sales = fdf["sales"].sum()
total_profit = fdf["profit"].sum()
order_count = fdf["order_id"].nunique()
aov = (fdf.groupby("order_id")["sales"].sum().mean()) if order_count > 0 else 0.0
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Sales", f"₹{total_sales:,.0f}")
kpi2.metric("Total Profit", f"₹{total_profit:,.0f}")
kpi3.metric("Avg Order Value", f"₹{aov:,.0f}")
kpi4.metric("Profit Margin", f"{profit_margin:.1f}%")

st.markdown("---")

# ---- CHARTS ----

# 1) Sales trend over time
ts = fdf.resample("M", on="order_date")["sales"].sum().reset_index()
fig_ts = px.line(ts, x="order_date", y="sales", markers=True, title="Monthly Sales Trend")
st.plotly_chart(fig_ts, use_container_width=True)

# 2) Sales by Category
cat = fdf.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
fig_cat = px.bar(cat, x="category", y="sales", title="Sales by Category")
st.plotly_chart(fig_cat, use_container_width=True)

# 3) Top 10 Products by Sales
prod = (fdf.groupby(["product_id", "product_name"], as_index=False)["sales"]
        .sum().sort_values("sales", ascending=False).head(10))
fig_prod = px.bar(prod, x="sales", y="product_name", orientation="h", title="Top 10 Products by Sales")
st.plotly_chart(fig_prod, use_container_width=True)

# 4) Heatmap: Month vs Region
heat = fdf.pivot_table(index="month_name", columns="region", values="sales", aggfunc="sum").fillna(0)
# ensure calendar order for months
month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]
heat = heat.reindex(month_order)
heat_reset = heat.reset_index().melt(id_vars="month_name", var_name="region", value_name="sales")
fig_heat = px.density_heatmap(heat_reset, x="region", y="month_name", z="sales", nbinsx=4, nbinsy=12, title="Sales Heatmap (Month vs Region)")
st.plotly_chart(fig_heat, use_container_width=True)

# ---- TABLE: Detail view ----
st.subheader("Detailed Transactions (filtered)")
st.dataframe(fdf.sort_values("order_date", ascending=False).head(500))
