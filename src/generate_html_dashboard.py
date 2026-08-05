"""
Script to generate an interactive HTML Power BI Dashboard Preview
"""

import os
import json
import pandas as pd

def generate_interactive_dashboard(csv_path, output_html_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    # Aggregations for JS Chart embedded data
    cat_agg = df.groupby('category').agg(
        revenue=('total_revenue', 'sum'),
        units=('units_sold', 'sum')
    ).reset_index().to_dict(orient='records')

    seller_agg = df.groupby('seller').agg(
        revenue=('total_revenue', 'sum'),
        units=('units_sold', 'sum'),
        rating=('seller_rating', 'mean')
    ).reset_index().sort_values(by='revenue', ascending=False).to_dict(orient='records')

    disc_agg = df.groupby('discount_tier', observed=False).agg(
        revenue=('total_revenue', 'sum'),
        units=('units_sold', 'sum'),
        count=('product_id', 'count'),
        loss=('total_discount_loss', 'sum')
    ).reset_index().to_dict(orient='records')

    payment_agg = df.groupby('payment_modes').agg(
        revenue=('total_revenue', 'sum'),
        units=('units_sold', 'sum')
    ).reset_index().to_dict(orient='records')

    top_10 = df.sort_values(by='total_revenue', ascending=False).head(10)[[
        'product_id', 'product_name', 'category', 'seller', 'price', 'discount_percent', 'final_price', 'units_sold', 'total_revenue', 'rating'
    ]].to_dict(orient='records')

    bottom_10 = df[df['performance_segment'] == 'Underperformer'].sort_values(by=['units_sold', 'stock_available'], ascending=[True, False]).head(10)[[
        'product_id', 'product_name', 'category', 'seller', 'price', 'stock_available', 'units_sold', 'rating'
    ]].to_dict(orient='records')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-commerce Sales Power BI Interactive Dashboard</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.85);
            --card-border: rgba(255, 255, 255, 0.1);
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.3);
            --secondary: #818cf8;
            --accent-green: #34d399;
            --accent-red: #f87171;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            padding: 24px;
            min-height: 100vh;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--card-border);
        }}
        
        .header h1 {{
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .badge {{
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        }}
        
        .tab-btn {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .tab-btn:hover, .tab-btn.active {{
            background: var(--primary);
            color: #000;
            font-weight: 600;
            box-shadow: 0 0 15px var(--primary-glow);
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
            transition: transform 0.2s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: var(--primary);
        }}
        
        .kpi-title {{
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .kpi-value {{
            font-size: 26px;
            font-weight: 700;
            color: var(--text-main);
        }}

        .kpi-subtext {{
            font-size: 12px;
            color: var(--accent-green);
            margin-top: 6px;
        }}
        
        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 24px;
        }}

        @media (max-width: 992px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .chart-card h3 {{
            font-size: 16px;
            margin-bottom: 16px;
            color: var(--text-main);
        }}
        
        .canvas-container {{
            position: relative;
            height: 300px;
            width: 100%;
        }}

        /* Table Design */
        .table-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        th, td {{
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--card-border);
        }}

        th {{
            color: var(--text-muted);
            font-weight: 600;
            background: rgba(15, 23, 42, 0.6);
        }}

        tr:hover {{
            background: rgba(56, 189, 248, 0.05);
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>E-commerce Sales & Analytics Power BI Dashboard</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Created by <strong>Upendra Pal</strong> | Executive Performance Preview & Dynamic Visualizer</p>
        </div>
        <div class="badge">Author: Upendra Pal</div>
    </div>

    <!-- Navigation Tabs -->
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('overview')">1. Sales Overview</button>
        <button class="tab-btn" onclick="switchTab('products')">2. Product Performance</button>
        <button class="tab-btn" onclick="switchTab('discounts')">3. Price & Discounts</button>
        <button class="tab-btn" onclick="switchTab('sellers')">4. Seller Metrics</button>
    </div>

    <!-- TAB 1: SALES OVERVIEW -->
    <div id="tab-overview" class="tab-content active">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">$4.76 Trillion</div>
                <div class="kpi-subtext">Across 80,000 SKUs</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total Units Sold</div>
                <div class="kpi-value">200.6 Million</div>
                <div class="kpi-subtext">Avg 2,507 units/product</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Order Price</div>
                <div class="kpi-value">$23,738</div>
                <div class="kpi-subtext">Net after discounts</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Gross Discount Loss</div>
                <div class="kpi-value">$1.29 Trillion</div>
                <div class="kpi-subtext" style="color: var(--accent-red)">21.35% Average Discount</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Revenue by Category ($ Billions)</h3>
                <div class="canvas-container">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>Revenue by Payment Mode ($ Billions)</h3>
                <div class="canvas-container">
                    <canvas id="paymentChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: PRODUCT PERFORMANCE -->
    <div id="tab-products" class="tab-content">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Listed SKUs</div>
                <div class="kpi-value">80,000</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Best-Seller SKUs</div>
                <div class="kpi-value" style="color: var(--accent-green)">16,011</div>
                <div class="kpi-subtext">Top 20% by Volume</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Underperformer SKUs</div>
                <div class="kpi-value" style="color: var(--accent-red)">16,008</div>
                <div class="kpi-subtext">Bottom 20% by Volume</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Stranded Inventory Units</div>
                <div class="kpi-value">8.0 Million</div>
                <div class="kpi-subtext">Underperforming Stock</div>
            </div>
        </div>

        <div class="table-card">
            <h3 style="margin-bottom: 16px;">Top 10 Star Products (Best Sellers by Revenue)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Product Name</th>
                        <th>Category</th>
                        <th>Seller</th>
                        <th>Price ($)</th>
                        <th>Final Price ($)</th>
                        <th>Units Sold</th>
                        <th>Total Revenue ($)</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f"<tr><td>{p['product_id']}</td><td>{p['product_name']}</td><td>{p['category']}</td><td>{p['seller']}</td><td>${p['price']:,.2f}</td><td>${p['final_price']:,.2f}</td><td>{p['units_sold']:,}</td><td style='color:var(--accent-green); font-weight:600;'>${p['total_revenue']:,.2f}</td></tr>" for p in top_10])}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 3: PRICE & DISCOUNTS -->
    <div id="tab-discounts" class="tab-content">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Average Discount %</div>
                <div class="kpi-value">21.35%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Low Discount Share (0-10%)</div>
                <div class="kpi-value" style="color: var(--accent-green)">45.07%</div>
                <div class="kpi-subtext">$2.15T Revenue</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Deep Discount Share (>40%)</div>
                <div class="kpi-value" style="color: var(--accent-red)">8.05%</div>
                <div class="kpi-subtext">$383.3B Revenue</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Revenue Contribution by Discount Tier ($ Billions)</h3>
                <div class="canvas-container">
                    <canvas id="discountChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>Average Sales Volume per SKU by Discount Tier</h3>
                <div class="canvas-container">
                    <canvas id="discountVolumeChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 4: SELLER METRICS -->
    <div id="tab-sellers" class="tab-content">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Marketplace Sellers</div>
                <div class="kpi-value">8 Active Sellers</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Top Seller Share</div>
                <div class="kpi-value" style="color: var(--primary)">12.69%</div>
                <div class="kpi-subtext">UrbanRetails ($604B)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Average Seller Rating</div>
                <div class="kpi-value">4.00 / 5.00</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card" style="grid-column: span 2;">
                <h3>Seller Revenue Leaderboard ($ Billions)</h3>
                <div class="canvas-container">
                    <canvas id="sellerChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        // Data from python
        const catData = {json.dumps(cat_agg)};
        const sellerData = {json.dumps(seller_agg)};
        const discData = {json.dumps(disc_agg)};
        const paymentData = {json.dumps(payment_agg)};

        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'bar',
            data: {{
                labels: catData.map(d => d.category),
                datasets: [{{
                    label: 'Revenue ($ Billions)',
                    data: catData.map(d => (d.revenue / 1e9).toFixed(2)),
                    backgroundColor: '#38bdf8',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Payment Chart
        new Chart(document.getElementById('paymentChart'), {{
            type: 'doughnut',
            data: {{
                labels: paymentData.map(d => d.payment_modes),
                datasets: [{{
                    data: paymentData.map(d => (d.revenue / 1e9).toFixed(2)),
                    backgroundColor: ['#38bdf8', '#818cf8', '#34d399', '#f87171']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }}
            }}
        }});

        // Discount Revenue Chart
        new Chart(document.getElementById('discountChart'), {{
            type: 'bar',
            data: {{
                labels: discData.map(d => d.discount_tier),
                datasets: [{{
                    label: 'Total Revenue ($ Billions)',
                    data: discData.map(d => (d.revenue / 1e9).toFixed(2)),
                    backgroundColor: ['#34d399', '#38bdf8', '#818cf8', '#f87171'],
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Discount Volume Chart
        new Chart(document.getElementById('discountVolumeChart'), {{
            type: 'line',
            data: {{
                labels: discData.map(d => d.discount_tier),
                datasets: [{{
                    label: 'Avg Units Sold / SKU',
                    data: discData.map(d => (d.units / d.count).toFixed(1)),
                    borderColor: '#818cf8',
                    backgroundColor: 'rgba(129, 140, 248, 0.2)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ labels: {{ color: '#f8fafc' }} }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Seller Leaderboard Chart
        new Chart(document.getElementById('sellerChart'), {{
            type: 'bar',
            data: {{
                labels: sellerData.map(d => d.seller),
                datasets: [{{
                    label: 'Total Revenue ($ Billions)',
                    data: sellerData.map(d => (d.revenue / 1e9).toFixed(2)),
                    backgroundColor: '#818cf8',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Interactive HTML Dashboard generated at: {output_html_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_ecommerce_data.csv")
    HTML_PATH = os.path.join(BASE_DIR, "power_bi", "interactive_dashboard_preview.html")
    generate_interactive_dashboard(CSV_PATH, HTML_PATH)
