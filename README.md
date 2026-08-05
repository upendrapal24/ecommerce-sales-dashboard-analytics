# 🛒 E-commerce Sales Dashboard & Analytics

**Author**: **Upendra Pal** ([@upendrapal24](https://github.com/upendrapal24))  
**Repository**: [https://github.com/upendrapal24/ecommerce-sales-dashboard-analytics.git](https://github.com/upendrapal24/ecommerce-sales-dashboard-analytics.git)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Interactive%20Dashboard-F2C811?logo=powerbi&logoColor=black)
![Author](https://img.shields.io/badge/Author-Upendra%20Pal-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end data analytics project examining an e-commerce platform dataset of **80,000 products** and **$4.76 Trillion** in total revenue created by **Upendra Pal**. This project covers data cleaning in Python (Pandas), SQL pattern analysis, DAX calculations, an interactive Power BI dashboard visualizer, and executive business recommendations.


---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Data Insights](#-key-data-insights)
- [Repository Architecture](#-repository-architecture)
- [Installation & Setup](#-installation--setup)
- [Python Data Pipeline](#-python-data-pipeline)
- [SQL Analytics Suite](#-sql-analytics-suite)
- [Power BI Dashboard & DAX](#-power-bi-dashboard--dax)
- [Interactive Web Preview](#-interactive-web-preview)
- [Business Recommendations](#-business-recommendations)
- [How to Upload to GitHub](#-how-to-upload-to-github)

---

## 📊 Project Overview

This repository addresses critical business questions regarding e-commerce platform performance:
1. **Sales Overview**: Revenue distribution across categories, price tiers, and payment channels.
2. **Product Performance**: Identifying top star SKUs vs. underperforming inventory locking up capital.
3. **Discount Impact**: Econometric analysis of price elasticity and gross margin erosion.
4. **Seller Performance**: Evaluating seller concentration, ratings, and marketplace health.

---

## 📈 Key Data Insights

- **Total Revenue**: `$4,761,907,956,925.44` (~$4.76 Trillion) across **200,601,262 units sold**.
- **Top Categories**: **Toys** ($606.45B) and **Beauty** ($605.82B) lead platform sales.
- **Discount Inefficiency**: Deep discounts (>40%) deliver only **2,522 units/product** vs **2,510 units/product** at 0-10% discount, proving that deep discounts destroy margin without increasing demand.
- **Stranded Capital**: **16,008 SKUs** are classified as underperformers with over **8.0M units** sitting idle in inventory.

---

## 📁 Repository Architecture

```
E-commerce Sales Dashboard & Analytics/
├── data/
│   ├── cleaned_ecommerce_data.csv        # Cleaned dataset (80,000 rows x 33 cols)
│   └── ecommerce_sales.db               # SQLite database with indexes
├── src/
│   ├── data_cleaning.py                 # Automated Pandas cleaning script
│   ├── run_sql_queries.py               # SQL execution engine
│   ├── generate_notebook.py             # Jupyter notebook generator
│   └── generate_html_dashboard.py       # Interactive web preview builder
├── notebooks/
│   └── ecommerce_data_cleaning_and_eda.ipynb  # Interactive Jupyter Notebook
├── sql/
│   └── sales_pattern_analysis.sql       # 8 comprehensive analytical SQL queries
├── power_bi/
│   ├── dax_measures.dax                 # Complete DAX formulas for Power BI
│   ├── dashboard_design_guide.md        # Layout & visual design documentation
│   └── interactive_dashboard_preview.html # Web-based interactive dashboard
├── reports/
│   └── business_recommendations_report.md  # Executive strategic report
├── README.md                            # Main project documentation
└── .gitignore                           # Git ignore rules
```

---

## 🚀 Installation & Setup

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/upendrapal24/ecommerce-sales-dashboard-analytics.git
cd ecommerce-sales-dashboard-analytics
pip install pandas numpy matplotlib seaborn
```

### 2. Run Data Cleaning & Build Database
```bash
python src/data_cleaning.py
```

### 3. Run SQL Queries
```bash
python src/run_sql_queries.py
```

---

## 💻 Python Data Pipeline

The data cleaning pipeline (`src/data_cleaning.py`):
- Validates missing values and sanitizes string formatting.
- Converts dates into standardized format (`YYYY-MM-DD`) and extracts `listing_year`, `listing_month`, `listing_year_month`.
- Computes derived metrics: `gross_revenue`, `total_revenue`, `discount_amount`, `total_discount_loss`.
- Categorizes products into **Price Tiers**, **Discount Tiers**, and **Performance Segments**.
- Saves cleaned dataset to `data/cleaned_ecommerce_data.csv` and populates SQLite database `data/ecommerce_sales.db`.

---

## 🛢️ SQL Analytics Suite

SQL queries in `sql/sales_pattern_analysis.sql` cover:
- Executive Sales Summary
- Top Seller Revenue Share & Leaderboard
- Discount Tier Impact & Elasticity
- Category Performance Matrix
- Top 10 Best Sellers vs. Underperforming Inventory
- Payment Mode & Delivery Time Logistics

#### Sample SQL Query (Discount Tier Impact):
```sql
SELECT 
    discount_tier,
    COUNT(product_id) AS total_products,
    SUM(units_sold) AS total_units_sold,
    ROUND(AVG(units_sold), 1) AS avg_units_per_product,
    ROUND(SUM(total_revenue), 2) AS total_revenue_usd,
    ROUND(SUM(total_discount_loss), 2) AS gross_discount_cost_usd
FROM sales
GROUP BY discount_tier
ORDER BY total_revenue_usd DESC;
```

---

## 💛 Power BI Dashboard & DAX

The Power BI model includes custom DAX measures in `power_bi/dax_measures.dax`:

```dax
Total Revenue = SUMX(sales, sales[final_price] * sales[units_sold])

Discount Loss Percentage = DIVIDE([Total Discount Loss], [Total Gross Revenue], 0)

Seller Revenue Rank = RANKX(ALLSELECTED(sales[seller]), [Total Revenue], , DESC, Dense)
```

The dashboard features 4 key pages:
1. **Sales Overview**: Revenue KPIs, Category Distribution, Payment Modes.
2. **Product Performance**: Best-Sellers vs Underperforming Products Matrix.
3. **Price-Discount Analysis**: Elasticity Scatter Plot, Discount Loss Tiers.
4. **Seller Performance Metrics**: Seller Ranking Leaderboard & Rating Correlations.

---

## 🌐 Interactive Web Preview

Preview the dashboard live in your browser by opening:
`power_bi/interactive_dashboard_preview.html`

Features:
- Dark Glassmorphism Design Theme.
- Responsive Chart.js visualizations (Category Bar Chart, Payment Mode Donut, Discount Column Chart, Seller Leaderboard).
- Tabbed Navigation matching Power BI page structure.

---

## 💡 Business Recommendations

1. **Cap Maximum Discount at 25%**: Eliminate discounts >25% to preserve over $300B in gross margins without sacrificing sales volume.
2. **Automate Clearance for Dead Stock**: Liquidate 16,008 underperforming SKUs carrying over 8.0M units in stranded stock.
3. **Focus Marketing on Toys & Beauty**: Double down on high-performing product categories driving platform revenue.
4. **Enforce Seller Quality SLAs**: Implement seller rating thresholds (>4.2) and penalize delivery delays.

---

## 📤 How to Upload to GitHub

Follow these simple commands to push this project to your GitHub repository:

```bash
# 1. Initialize git repository
git init

# 2. Add all project files
git add .

# 3. Commit files
git commit -m "Initial commit: E-commerce Sales Dashboard & Analytics Project"

# 4. Set main branch
git branch -M main

# 5. Add remote GitHub URL
git remote add origin https://github.com/upendrapal24/ecommerce-sales-dashboard-analytics.git

# 6. Push to GitHub
git push -u origin main
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
