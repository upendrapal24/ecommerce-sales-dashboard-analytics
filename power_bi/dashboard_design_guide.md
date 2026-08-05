# Power BI Interactive Dashboard Design Guide

**Author**: Upendra Pal ([@upendrapal24](https://github.com/upendrapal24))

## 1. Executive Summary & Architecture
This document provides full specifications for building the **E-commerce Sales & Performance Analytics Power BI Dashboard**. The design adopts a **Dark Glassmorphism aesthetic** tailored for executive presentations and interactive decision-making.

---

## 2. Canvas & Design Theme System

### Canvas Settings
- **Page Size**: 16:9 Widescreen (1920 x 1080 px)
- **Background**: `#0F172A` (Deep Slate / Dark Mode)
- **Card Fill / Container**: `#1E293B` with 80% opacity and subtle `#334155` border (Glassmorphism look)
- **Accent Palette**:
  - Primary Accent: `#38BDF8` (Electric Sky Blue)
  - Secondary Accent: `#818CF8` (Violet Purple)
  - Positive / Growth: `#34D399` (Emerald Green)
  - Warning / Underperformer: `#F87171` (Coral Red)
  - Neutral / Muted Text: `#94A3B8` (Slate Silver)

### Typography
- **Header Font**: Segoe UI Semibold / Bold
- **KPI Number Font**: Segoe UI Bold (Size 28-36 pt)
- **Body & Axis Labels**: Segoe UI Regular (Size 10-12 pt)

---

## 3. Multi-Page Layout & Visual Blueprint

The Power BI Dashboard consists of **4 main interactive pages**:

```
+------------------------------------------------------------------------------------+
|                                POWER BI NAV BAR                                    |
| [1. Sales Overview] | [2. Product Performance] | [3. Price & Discounts] | [4. Sellers] |
+------------------------------------------------------------------------------------+
```

---

### Page 1: Sales Overview (Revenue & Orders)

#### Purpose
High-level operational breakdown of gross vs net revenue, unit sales volume, category revenue contribution, and payment channel preference.

#### Visual Layout Grid:
1. **Top Header Slicers**:
   - `Category` (Dropdown)
   - `Price Tier` (Tile Buttons)
   - `Seller City` (Dropdown)
   - `Listing Date Range` (Date Slider)

2. **KPI Header Cards (Row 1)**:
   - **Card 1**: Total Revenue (`$4.76T`)
   - **Card 2**: Total Units Sold (`200.6M`)
   - **Card 3**: Average Order Value / Price (`$23.7K`)
   - **Card 4**: Gross Discount Loss (`$1.29T` / `21.35% Avg`)

3. **Main Visuals (Row 2 & 3)**:
   - **Visual 1 (Donut Chart)**: Revenue Breakdown by Category (Toys, Beauty, Fashion, Electronics, etc.)
   - **Visual 2 (Clustered Bar Chart)**: Total Revenue by Payment Mode (`UPI, CARD`, `CARD, Wallet`, `COD, UPI, CARD`, `COD, CARD`)
   - **Visual 3 (Line Chart)**: Monthly Sales Trend (`listing_year_month` vs Total Revenue & Units Sold)
   - **Visual 4 (Bar Chart)**: Revenue Contribution by Price Tier (Budget, Mid-Range, Premium, Luxury)

---

### Page 2: Best-Selling & Underperforming Products

#### Purpose
Granular SKU analysis to separate star products from capital-locking dead inventory.

#### Visual Layout Grid:
1. **KPI Header Cards**:
   - Total Listed SKUs (`80,000`)
   - Best-Seller Count (`16,011`)
   - Underperformer Count (`16,008`)
   - Dead Stock Units Locked (`10.2M Units`)

2. **Main Visuals**:
   - **Visual 1 (Scatter Plot)**: Units Sold (Y-axis) vs Price (X-axis) colored by Category (Bubble size = Revenue). Highlighting the high-volume quadrant.
   - **Visual 2 (Top 10 Horizontal Bar Chart)**: Top 10 Best-Selling SKUs by Revenue.
   - **Visual 3 (Bottom 10 Horizontal Bar Chart)**: Top 10 Underperforming SKUs with zero units sold and high stock levels.
   - **Visual 4 (Matrix Table)**: Detailed SKU Audit table with `product_name`, `category`, `price`, `stock_available`, `units_sold`, `total_revenue`, `rating`, and `performance_segment`.

---

### Page 3: Price-Discount Analysis

#### Purpose
Quantifying discount elasticity and margin erosion to establish optimal discount boundaries.

#### Visual Layout Grid:
1. **KPI Header Cards**:
   - Average Discount Percentage (`21.35%`)
   - Gross Discount Loss (`$1.29T`)
   - Revenue Share under Deep Discounts (`8.05%`)
   - Profit Erosion Factor

2. **Main Visuals**:
   - **Visual 1 (Column & Line Combo Chart)**: Units Sold (Bars) and Revenue Loss (Line) across Discount Tiers (`0-10%`, `11-25%`, `26-40%`, `>40%`).
   - **Visual 2 (Clustered Bar Chart)**: Average Discount % vs Average Rating by Category.
   - **Visual 3 (Scatter Plot)**: Discount % vs Units Sold to prove elasticity curves.

---

### Page 4: Seller Performance Metrics

#### Purpose
Evaluating seller marketplace health, ratings, volume concentration, and fulfillment reliability.

#### Visual Layout Grid:
1. **KPI Header Cards**:
   - Total Active Sellers (`8 Key Marketplace Sellers`)
   - Average Seller Rating (`4.00 / 5.00`)
   - Top 5 Seller Revenue Concentration (`62.4%`)

2. **Main Visuals**:
   - **Visual 1 (Leaderboard Bar Chart)**: Total Revenue by Seller (`UrbanRetails`, `QuickShop`, `BestBuy`, `SuperMart`, `ValueKart`, etc.).
   - **Visual 2 (Scatter Plot)**: Seller Rating (X-axis) vs Total Units Sold (Y-axis).
   - **Visual 3 (Map / City Bar Chart)**: Seller Revenue by City (`Bengaluru`, `Delhi`, `Mumbai`, `Hyderabad`).

---

## 4. How to Import and Build in Power BI Desktop

1. **Import Data**:
   - Open Power BI Desktop -> `Get Data` -> `Text/CSV` -> Select `data/cleaned_ecommerce_data.csv`.
2. **Apply DAX Measures**:
   - Go to `Model View` -> Create a new `_Measures` table -> Copy & paste DAX code from `power_bi/dax_measures.dax`.
3. **Apply Theme**:
   - Go to `View` tab -> `Themes` -> Import theme or configure dark theme colors (`#0F172A`, `#1E293B`, `#38BDF8`).
4. **Publishing**:
   - Publish to Power BI Service -> Set up scheduled refresh -> Pin key visual cards to Executive Dashboard.
