"""
Script to execute SQL queries in sql/sales_pattern_analysis.sql against SQLite database
"""

import os
import sqlite3
import pandas as pd

def run_sql_suite(db_path, sql_file_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    if not os.path.exists(sql_file_path):
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    conn = sqlite3.connect(db_path)
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by semicolon to execute queries individually
    queries = [q.strip() for q in sql_content.split(';') if q.strip()]
    
    print(f"Executing {len(queries)} SQL Queries from {os.path.basename(sql_file_path)}...")
    print("=" * 70)

    query_titles = [
        "1. Executive Sales Summary",
        "2. Top Seller Leaderboard",
        "3. Discount Impact Analysis",
        "4. Category Performance Matrix",
        "5. Top 10 Best-Selling Products",
        "6. Underperforming Inventory Audit",
        "7. Price Tier Breakdown",
        "8. Payment Modes & Logistics"
    ]

    for idx, query in enumerate(queries):
        title = query_titles[idx] if idx < len(query_titles) else f"Query {idx+1}"
        print(f"\n--- {title} ---")
        try:
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Error executing query {idx+1}: {e}")
            
    conn.close()
    print("=" * 70)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce_sales.db")
    SQL_PATH = os.path.join(BASE_DIR, "sql", "sales_pattern_analysis.sql")
    run_sql_suite(DB_PATH, SQL_PATH)
