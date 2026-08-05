"""
E-commerce Sales Data Cleaning and Transformation Script
Author: Upendra Pal (github.com/upendrapal24)
Description: Cleans raw e-commerce data, handles data types, derives key analytical metrics,
             and loads cleaned records into CSV and an SQLite database for SQL analysis.
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def clean_ecommerce_data(input_path: str, output_csv_path: str, db_path: str):
    print("=" * 60)
    print("STARTING E-COMMERCE DATA CLEANING PIPELINE")
    print("=" * 60)

    # 1. Load Raw Data
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")
    
    print(f"[1/5] Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"      Initial record count: {initial_rows:,} rows, {len(df.columns)} columns")

    # 2. Data Cleaning & Sanitization
    print("[2/5] Cleaning data and removing duplicates/nulls...")
    
    # Strip string white spaces
    str_cols = df.select_dtypes(include=['object']).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # Drop duplicate rows if any
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"      Removed {duplicates} duplicate rows.")
    else:
        print("      No duplicate rows found.")

    # Fill missing values if any
    null_summary = df.isnull().sum()
    if null_summary.sum() > 0:
        print(f"      Handling missing values:\n{null_summary[null_summary > 0]}")
        # Numeric missing -> median
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        # Categorical missing -> 'Unknown'
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('Unknown')
    else:
        print("      No missing values found.")

    # 3. Data Type Formatting & Derived Fields
    print("[3/5] Parsing dates and calculating analytical features...")
    
    # Convert listing_date
    df['listing_date'] = pd.to_datetime(df['listing_date'], errors='coerce')
    df['listing_year'] = df['listing_date'].dt.year
    df['listing_month'] = df['listing_date'].dt.month
    df['listing_year_month'] = df['listing_date'].dt.strftime('%Y-%m')
    df['listing_date'] = df['listing_date'].dt.strftime('%Y-%m-%d')

    # Recalculate price fields to ensure mathematical consistency
    df['calculated_final_price'] = (df['price'] * (1 - df['discount_percent'] / 100)).round(2)
    df['discount_amount'] = (df['price'] - df['final_price']).round(2)
    
    # Revenue calculations
    df['total_revenue'] = (df['final_price'] * df['units_sold']).round(2)
    df['gross_revenue'] = (df['price'] * df['units_sold']).round(2)
    df['total_discount_loss'] = (df['discount_amount'] * df['units_sold']).round(2)

    # Categorical Bins: Price Tiers
    price_bins = [-1, 15000, 35000, 50000, np.inf]
    price_labels = ['Budget (<15k)', 'Mid-Range (15k-35k)', 'Premium (35k-50k)', 'Luxury (>50k)']
    df['price_tier'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)

    # Categorical Bins: Discount Tiers
    discount_bins = [-1, 10, 25, 40, np.inf]
    discount_labels = ['Low (0-10%)', 'Moderate (11-25%)', 'High (26-40%)', 'Deep Discount (>40%)']
    df['discount_tier'] = pd.cut(df['discount_percent'], bins=discount_bins, labels=discount_labels)

    # Performance Segmentation based on Units Sold percentiles
    p20 = df['units_sold'].quantile(0.20)
    p80 = df['units_sold'].quantile(0.80)
    
    def segment_product(row):
        if row['units_sold'] >= p80:
            return 'Best-Seller'
        elif row['units_sold'] <= p20:
            return 'Underperformer'
        else:
            return 'Moderate'
            
    df['performance_segment'] = df.apply(segment_product, axis=1)

    # 4. Export Clean Data to CSV
    print(f"[4/5] Exporting clean data to CSV: {output_csv_path}...")
    output_dir = os.path.dirname(output_csv_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print("      CSV export completed successfully.")

    # 5. Export to SQLite Database for SQL Querying
    print(f"[5/5] Creating SQLite database at {db_path}...")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    # Create indexes for optimization
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_seller ON sales(seller);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_performance ON sales(performance_segment);")
    conn.commit()
    conn.close()
    
    print("      SQLite database & indexes built successfully.")
    
    # Summary Output
    print("=" * 60)
    print("DATA PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Total Products Processed : {len(df):,}")
    print(f"Total Revenue Generated   : ${df['total_revenue'].sum():,.2f}")
    print(f"Total Units Sold          : {df['units_sold'].sum():,}")
    print(f"Average Order Discount %  : {df['discount_percent'].mean():.2f}%")
    print(f"Best-Selling Products    : {(df['performance_segment']=='Best-Seller').sum():,}")
    print(f"Underperforming Products  : {(df['performance_segment']=='Underperformer').sum():,}")
    print("=" * 60)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_PATH = os.path.join(BASE_DIR, "cleaned_ecommerce_data.csv")
    CLEAN_CSV = os.path.join(BASE_DIR, "data", "cleaned_ecommerce_data.csv")
    DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce_sales.db")
    
    clean_ecommerce_data(RAW_PATH, CLEAN_CSV, DB_PATH)
