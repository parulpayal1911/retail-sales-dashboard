# Retail Sales Performance Dashboard

An interactive dashboard that visualizes retail sales performance across regions, categories, and time periods.  
Built with **Streamlit**, **Pandas**, and **Plotly**. This is a customized, original version with a synthetic dataset and additional KPIs/visuals.

## ✨ Features
- KPI cards: Total Sales, Profit, Average Order Value, Profit Margin
- Filters: Date range, Region, Category, Payment Method
- Charts:
  - Monthly Sales Trend (line)
  - Sales by Category (bar)
  - Top 10 Products by Sales (horizontal bar)
  - Sales Heatmap (Month vs Region)
- Transaction table view (filtered)

## 🧪 Dataset
A custom-generated synthetic dataset with 12,000 transactions (2023–2025) across 4 regions and multiple product categories.  
File: `retail_sales.csv`

## 🚀 Quickstart
```bash
# 1) Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
streamlit run app.py
```

Then open the local URL Streamlit prints in your terminal.

## 📁 Project Structure
```
.
├── app.py
├── retail_sales.csv
├── requirements.txt
└── README.md
```

## 🧭 Notes
- This project intentionally differs from typical public retail dashboards:
  - Synthetic dataset and additional columns (payment_method, profit, etc.)
  - New visuals (heatmap, top products) and KPIs
  - Clear README and reproducible setup
- Feel free to replace `retail_sales.csv` with your own real dataset (same columns) to make it even more unique.

## 🌐 Deploy (optional)
- **Streamlit Cloud**: Push this repo to GitHub and deploy directly from the Streamlit dashboard.
- **Hugging Face Spaces**: Create a Space (Streamlit), point it to your repo.

## 📝 License
MIT (or add your preferred license).
