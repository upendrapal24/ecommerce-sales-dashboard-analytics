"""
Generate High-Resolution Power BI Dashboard Screenshot Images for GitHub README
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set dark theme styling for Power BI look
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'

os.makedirs('assets/images', exist_ok=True)
print("Loading dataset...", flush=True)
df = pd.read_csv('cleaned_ecommerce_data.csv')

# Compute derived columns if missing
if 'total_revenue' not in df.columns:
    df['total_revenue'] = df['final_price'] * df['units_sold']
if 'gross_revenue' not in df.columns:
    df['gross_revenue'] = df['price'] * df['units_sold']
if 'total_discount_loss' not in df.columns:
    df['total_discount_loss'] = (df['price'] - df['final_price']) * df['units_sold']

if 'discount_tier' not in df.columns:
    bins = [-1, 10, 25, 40, 100]
    labels = ['Low (0-10%)', 'Moderate (10-25%)', 'High (25-40%)', 'Deep (>40%)']
    df['discount_tier'] = pd.cut(df['discount_percent'], bins=bins, labels=labels)

if 'price_tier' not in df.columns:
    df['price_tier'] = pd.qcut(df['price'], q=4, labels=['Budget', 'Mid-Range', 'Premium', 'Ultra-Premium'])

if 'performance_segment' not in df.columns:
    rev_median = df['total_revenue'].median()
    units_median = df['units_sold'].median()
    def get_seg(row):
        if row['total_revenue'] >= rev_median and row['units_sold'] >= units_median:
            return 'Star Product'
        elif row['total_revenue'] >= rev_median:
            return 'High Value'
        elif row['units_sold'] >= units_median:
            return 'Volume Mover'
        else:
            return 'Underperformer'
    df['performance_segment'] = df.apply(get_seg, axis=1)

BG_COLOR = '#0f172a'
CARD_BG = '#1e293b'
ACCENT_BLUE = '#38bdf8'
ACCENT_INDIGO = '#818cf8'
ACCENT_GREEN = '#34d399'
ACCENT_RED = '#f87171'
ACCENT_YELLOW = '#fbbf24'
TEXT_MAIN = '#f8fafc'
TEXT_MUTED = '#94a3b8'

tot_rev_b = df['total_revenue'].sum() / 1e9
tot_units_m = df['units_sold'].sum() / 1e6
tot_disc_loss_b = df['total_discount_loss'].sum() / 1e9

# --- 1. SALES OVERVIEW DASHBOARD ---
fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
gs = fig.add_gridspec(3, 3, height_ratios=[0.25, 1, 1], hspace=0.35, wspace=0.25)

ax_head = fig.add_subplot(gs[0, :])
ax_head.set_facecolor(CARD_BG)
ax_head.axis('off')
ax_head.text(0.02, 0.6, "🛒 POWER BI DASHBOARD — Executive Sales Overview", fontsize=18, fontweight='bold', color=TEXT_MAIN, va='center')
ax_head.text(0.02, 0.25, "Real-time E-Commerce Platform Analytics | Author: Upendra Pal", fontsize=10, color=ACCENT_BLUE, va='center')

ax_c1 = fig.add_subplot(gs[0, 0])
ax_c1.set_facecolor('#1e293b')
ax_c1.axis('off')
ax_c1.text(0.5, 0.65, f"${tot_rev_b/1000:.2f} Trillion", fontsize=20, fontweight='bold', color=ACCENT_BLUE, ha='center', va='center')
ax_c1.text(0.5, 0.25, "TOTAL GROSS REVENUE", fontsize=8, fontweight='bold', color=TEXT_MUTED, ha='center', va='center')

ax_c2 = fig.add_subplot(gs[0, 1])
ax_c2.set_facecolor('#1e293b')
ax_c2.axis('off')
ax_c2.text(0.5, 0.65, f"{tot_units_m:.1f} Million", fontsize=20, fontweight='bold', color=ACCENT_GREEN, ha='center', va='center')
ax_c2.text(0.5, 0.25, "TOTAL UNITS SOLD", fontsize=8, fontweight='bold', color=TEXT_MUTED, ha='center', va='center')

ax_c3 = fig.add_subplot(gs[0, 2])
ax_c3.set_facecolor('#1e293b')
ax_c3.axis('off')
ax_c3.text(0.5, 0.65, f"${tot_disc_loss_b:.1f} Billion", fontsize=20, fontweight='bold', color=ACCENT_RED, ha='center', va='center')
ax_c3.text(0.5, 0.25, "GROSS DISCOUNT MARGIN EROSION", fontsize=8, fontweight='bold', color=TEXT_MUTED, ha='center', va='center')

ax1 = fig.add_subplot(gs[1, 0:2])
ax1.set_facecolor(CARD_BG)
cat_rev = df.groupby('category')['total_revenue'].sum().sort_values(ascending=True) / 1e9
bars = ax1.barh(cat_rev.index, cat_rev.values, color=ACCENT_BLUE, height=0.6)
ax1.set_title("Revenue by Product Category ($ Billion)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax1.set_xlabel("Revenue ($ Billion)", color=TEXT_MUTED, fontsize=9)
ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
for bar in bars:
    ax1.text(bar.get_width() + (cat_rev.max()*0.02), bar.get_y() + bar.get_height()/2, f"${bar.get_width():.1f}B", va='center', color=TEXT_MAIN, fontsize=8, fontweight='bold')

ax2 = fig.add_subplot(gs[1, 2])
ax2.set_facecolor(CARD_BG)
df['primary_payment'] = df['payment_modes'].apply(lambda x: str(x).split(',')[0] if pd.notna(x) else 'Other')
pay_rev = df.groupby('primary_payment')['total_revenue'].sum()
colors = [ACCENT_BLUE, ACCENT_INDIGO, ACCENT_GREEN, ACCENT_YELLOW, ACCENT_RED]
wedges, texts, autotexts = ax2.pie(pay_rev, labels=pay_rev.index, autopct='%1.1f%%', colors=colors[:len(pay_rev)], startangle=140, textprops=dict(color=TEXT_MAIN, fontsize=8), wedgeprops=dict(width=0.4, edgecolor=BG_COLOR))
for at in autotexts:
    at.set_color('#000000')
    at.set_fontweight('bold')
ax2.set_title("Revenue Share by Payment Method", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)

ax3 = fig.add_subplot(gs[2, :])
ax3.set_facecolor(CARD_BG)
disc_summary = df.groupby('discount_tier', observed=False).agg({'total_revenue': lambda x: x.sum()/1e9, 'total_discount_loss': lambda x: x.sum()/1e9})
x = np.arange(len(disc_summary))
width = 0.35
ax3.bar(x - width/2, disc_summary['total_revenue'], width, label='Revenue ($B)', color=ACCENT_BLUE)
ax3.bar(x + width/2, disc_summary['total_discount_loss'], width, label='Discount Loss ($B)', color=ACCENT_RED)
ax3.set_title("Discount Tier Breakdown: Revenue vs Margin Loss ($ Billion)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax3.set_xticks(x)
ax3.set_xticklabels(disc_summary.index, color=TEXT_MUTED, fontsize=9)
ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
ax3.legend(facecolor=CARD_BG, edgecolor='#334155', labelcolor=TEXT_MAIN, fontsize=8)

plt.tight_layout()
plt.savefig('assets/images/dashboard_sales_overview.png', dpi=140, bbox_inches='tight')
plt.close()
print("Saved dashboard_sales_overview.png", flush=True)

# --- 2. PRODUCT PERFORMANCE DASHBOARD ---
fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.35, wspace=0.25)

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(CARD_BG)
top_10 = df.sort_values(by='total_revenue', ascending=False).head(10)
bars = ax1.barh(top_10['product_name'].str[:25], top_10['total_revenue'] / 1e6, color=ACCENT_GREEN, height=0.6)
ax1.set_title("⭐ Top 10 Best-Selling SKUs by Revenue ($ Million)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax1.set_xlabel("Revenue ($ Million)", color=TEXT_MUTED, fontsize=8)
ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
ax1.invert_yaxis()

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(CARD_BG)
under_cat = df[df['performance_segment'] == 'Underperformer'].groupby('category')['stock_available'].sum() / 1e6
ax2.bar(under_cat.index, under_cat.values, color=ACCENT_RED, width=0.5)
ax2.set_title("⚠️ Stranded Inventory in Underperforming Products (M Units)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax2.set_ylabel("Stock Units (Millions)", color=TEXT_MUTED, fontsize=8)
ax2.tick_params(colors=TEXT_MUTED, labelsize=8, rotation=25)

ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(CARD_BG)
sample_df = df.sample(n=2000, random_state=42)
ax3.scatter(sample_df['rating'], sample_df['units_sold'], alpha=0.4, color=ACCENT_YELLOW, edgecolors='none', s=15)
ax3.set_title("Product Rating vs. Units Sold", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax3.set_xlabel("Customer Rating (1 - 5)", color=TEXT_MUTED, fontsize=8)
ax3.set_ylabel("Units Sold", color=TEXT_MUTED, fontsize=8)
ax3.tick_params(colors=TEXT_MUTED, labelsize=8)

ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(CARD_BG)
pt_counts = df['price_tier'].value_counts()
ax4.pie(pt_counts, labels=pt_counts.index, autopct='%1.1f%%', colors=[ACCENT_BLUE, ACCENT_INDIGO, ACCENT_GREEN, ACCENT_YELLOW], startangle=90, textprops=dict(color=TEXT_MAIN, fontsize=8), wedgeprops=dict(width=0.4, edgecolor=BG_COLOR))
ax4.set_title("Product Distribution across Price Tiers", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)

plt.suptitle("🛒 POWER BI DASHBOARD — Product & Inventory Performance Analytics", fontsize=16, fontweight='bold', color=TEXT_MAIN, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('assets/images/dashboard_product_performance.png', dpi=140, bbox_inches='tight')
plt.close()
print("Saved dashboard_product_performance.png", flush=True)

# --- 3. PRICE & DISCOUNT ELASTICITY DASHBOARD ---
fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(CARD_BG)
disc_avg = df.groupby('discount_tier', observed=False)['units_sold'].mean()
bars = ax1.bar(disc_avg.index, disc_avg.values, color=ACCENT_INDIGO, width=0.5)
ax1.set_title("Average Sales per Product by Discount Tier (Elasticity)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax1.set_ylabel("Avg Units Sold / SKU", color=TEXT_MUTED, fontsize=8)
ax1.tick_params(colors=TEXT_MUTED, labelsize=8)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (disc_avg.max()*0.02), f"{bar.get_height():.0f}", ha='center', color=TEXT_MAIN, fontsize=8, fontweight='bold')

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(CARD_BG)
ax2.scatter(sample_df['discount_percent'], sample_df['total_discount_loss']/1e3, alpha=0.3, color=ACCENT_RED, s=15)
ax2.set_title("Discount % vs. Gross Margin Loss ($ K)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax2.set_xlabel("Discount Percentage (%)", color=TEXT_MUTED, fontsize=8)
ax2.set_ylabel("Margin Loss ($ Thousands)", color=TEXT_MUTED, fontsize=8)
ax2.tick_params(colors=TEXT_MUTED, labelsize=8)

ax3 = fig.add_subplot(gs[1, :])
ax3.set_facecolor(CARD_BG)
cat_loss = df.groupby('category').agg({'total_revenue': lambda x: x.sum()/1e9, 'total_discount_loss': lambda x: x.sum()/1e9})
x = np.arange(len(cat_loss))
width = 0.35
ax3.bar(x - width/2, cat_loss['total_revenue'], width, label='Total Revenue ($B)', color=ACCENT_BLUE)
ax3.bar(x + width/2, cat_loss['total_discount_loss'], width, label='Gross Discount Loss ($B)', color=ACCENT_RED)
ax3.set_title("Category Revenue vs. Discount Erosion ($ Billion)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax3.set_xticks(x)
ax3.set_xticklabels(cat_loss.index, color=TEXT_MUTED, fontsize=9)
ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
ax3.legend(facecolor=CARD_BG, edgecolor='#334155', labelcolor=TEXT_MAIN, fontsize=8)

plt.suptitle("🛒 POWER BI DASHBOARD — Price Elasticity & Discount Loss Analysis", fontsize=16, fontweight='bold', color=TEXT_MAIN, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('assets/images/dashboard_price_discount.png', dpi=140, bbox_inches='tight')
plt.close()
print("Saved dashboard_price_discount.png", flush=True)

# --- 4. SELLER ANALYTICS DASHBOARD ---
fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(CARD_BG)
top_sellers = df.groupby('seller')['total_revenue'].sum().sort_values(ascending=False).head(10) / 1e9
bars = ax1.bar(top_sellers.index, top_sellers.values, color=ACCENT_BLUE, width=0.5)
ax1.set_title("🏆 Top 10 Seller Leaderboard by Revenue ($ Billion)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax1.set_ylabel("Revenue ($ Billion)", color=TEXT_MUTED, fontsize=8)
ax1.tick_params(colors=TEXT_MUTED, labelsize=8, rotation=15)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (top_sellers.max()*0.02), f"${bar.get_height():.1f}B", ha='center', color=TEXT_MAIN, fontsize=8, fontweight='bold')

ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor(CARD_BG)
seller_summary = df.groupby('seller').agg({'total_revenue': lambda x: x.sum()/1e9, 'seller_rating': 'mean'})
ax2.scatter(seller_summary['seller_rating'], seller_summary['total_revenue'], color=ACCENT_YELLOW, s=50, alpha=0.8)
ax2.set_title("Seller Rating vs. Generated Revenue ($B)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax2.set_xlabel("Average Seller Rating", color=TEXT_MUTED, fontsize=8)
ax2.set_ylabel("Revenue ($ Billion)", color=TEXT_MUTED, fontsize=8)
ax2.tick_params(colors=TEXT_MUTED, labelsize=8)

ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor(CARD_BG)
seller_units = df.groupby('seller')['units_sold'].sum().sort_values(ascending=False).head(10) / 1e6
ax3.barh(seller_units.index, seller_units.values, color=ACCENT_GREEN, height=0.5)
ax3.set_title("Units Sold by Top 10 Sellers (Million Units)", fontsize=12, fontweight='bold', color=TEXT_MAIN, pad=10)
ax3.set_xlabel("Units Sold (Millions)", color=TEXT_MUTED, fontsize=8)
ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
ax3.invert_yaxis()

plt.suptitle("🛒 POWER BI DASHBOARD — Marketplace Seller Performance", fontsize=16, fontweight='bold', color=TEXT_MAIN, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('assets/images/dashboard_seller_leaderboard.png', dpi=140, bbox_inches='tight')
plt.close()
print("Saved dashboard_seller_leaderboard.png", flush=True)
print("SUCCESS: All 4 Dashboard preview images generated successfully!", flush=True)
