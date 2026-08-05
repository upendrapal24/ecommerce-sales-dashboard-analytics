"""
Script to generate Jupyter Notebook for E-commerce Data Cleaning and EDA
"""

import json
import os

def create_eda_notebook(notebook_path):
    nb_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# E-commerce Sales Data Cleaning & Exploratory Data Analysis (EDA)\n",
                    "**Objective:** Clean, transform, and analyze the e-commerce sales dataset to uncover key revenue drivers, seller trends, product performance, and discount sensitivity."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import sqlite3\n",
                    "\n",
                    "# Graphics settings\n",
                    "sns.set_theme(style='darkgrid')\n",
                    "plt.rcParams['figure.figsize'] = (12, 6)\n",
                    "print('Libraries imported successfully.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. Load Raw Dataset"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df = pd.read_csv('../data/cleaned_ecommerce_data.csv')\n",
                    "print(f'Dataset Shape: {df.shape}')\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. Dataset Overview & Data Quality Check"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "df.info()\n",
                    "print('\\nMissing Values:\\n', df.isnull().sum())\n",
                    "print(f'\\nDuplicates: {df.duplicated().sum()}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. Revenue & Category Analysis"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "cat_summary = df.groupby('category').agg(\n",
                    "    total_revenue=('total_revenue', 'sum'),\n",
                    "    total_units=('units_sold', 'sum'),\n",
                    "    avg_price=('price', 'mean'),\n",
                    "    avg_discount=('discount_percent', 'mean'),\n",
                    "    avg_rating=('rating', 'mean')\n",
                    ").sort_values(by='total_revenue', ascending=False)\n",
                    "\n",
                    "cat_summary['revenue_billions'] = cat_summary['total_revenue'] / 1e9\n",
                    "display(cat_summary)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. Seller Performance Analysis"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "seller_summary = df.groupby('seller').agg(\n",
                    "    total_revenue=('total_revenue', 'sum'),\n",
                    "    total_units=('units_sold', 'sum'),\n",
                    "    avg_seller_rating=('seller_rating', 'mean'),\n",
                    "    product_count=('product_id', 'count')\n",
                    ").sort_values(by='total_revenue', ascending=False)\n",
                    "\n",
                    "seller_summary['revenue_billions'] = seller_summary['total_revenue'] / 1e9\n",
                    "display(seller_summary)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. Discount Impact & Price Elasticity"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "disc_summary = df.groupby('discount_tier').agg(\n",
                    "    product_count=('product_id', 'count'),\n",
                    "    total_revenue=('total_revenue', 'sum'),\n",
                    "    avg_units_sold=('units_sold', 'mean'),\n",
                    "    avg_rating=('rating', 'mean')\n",
                    ").reset_index()\n",
                    "\n",
                    "display(disc_summary)"
                ]
            }
        ],
        "metadata": {
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb_content, f, indent=2)
    print(f"Notebook generated at: {notebook_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    NB_PATH = os.path.join(BASE_DIR, "notebooks", "ecommerce_data_cleaning_and_eda.ipynb")
    create_eda_notebook(NB_PATH)
