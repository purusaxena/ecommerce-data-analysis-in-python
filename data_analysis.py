import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean, readable style for plots
sns.set_theme(style="whitegrid")

# ==============================================================================
# SECTION 1: LOAD AND MERGE
# ==============================================================================
print("--- SECTION 1: LOADING AND MERGING DATA ---")
# Read CSV files and ensure dates are parsed correctly
df_sales = pd.read_csv('sales_data.csv', parse_dates=['Date'])
df_products = pd.read_csv('products_data.csv')

# Perform a standard inner merge on the common key 'ProductID'
df_merged = pd.merge(df_sales, df_products, on='ProductID', how='inner')

# Print core structural properties of our new combined dataframe
print(f"Dataset Shape: {df_merged.shape}")
print("\nData Fields and Types:")
print(df_merged.dtypes)
print("\nSummary Statistics for Numeric Columns:")
print(df_merged.describe())
print("\n")

# ==============================================================================
# SECTION 2: INTRODUCING AND CLEANING DATA QUALITY ISSUES
# ==============================================================================
print("--- SECTION 2: DATA CLEANING ---")
# Let's deliberately introduce realistic data flaws
# 1. Inject missing values into Revenue (5% of the data)
df_merged.loc[df_merged.sample(frac=0.05, random_state=10).index, 'Revenue'] = np.nan

# 2. Inject some exact duplicate rows (10 rows)
duplicates = df_merged.head(10).copy()
df_merged = pd.concat([df_merged, duplicates], ignore_index=True)

print(f"Before Cleaning - Total Rows: {len(df_merged)}")
print(f"Before Cleaning - Duplicate Rows Count: {df_merged.duplicated().sum()}")
print(f"Before Cleaning - Missing Revenue Values: {df_merged['Revenue'].isnull().sum()}")

# Execution of Cleaning Steps:
# Step A: Drop duplicate records
df_merged.drop_duplicates(inplace=True)

# Step B: Handle missing revenue values using Mean Imputation
mean_revenue = df_merged['Revenue'].mean()
df_merged['Revenue'] = df_merged['Revenue'].fillna(mean_revenue)

print(f"\nAfter Cleaning - Total Rows: {len(df_merged)}")
print(f"After Cleaning - Duplicate Rows Count: {df_merged.duplicated().sum()}")
print(f"After Cleaning - Missing Revenue Values: {df_merged['Revenue'].isnull().sum()}\n")

# ==============================================================================
# SECTION 3: FEATURE ENGINEERING & OUTLIERS
# ==============================================================================
print("--- SECTION 3: FEATURE ENGINEERING ---")
# 1. Extract basic date parts using the .dt accessor
df_merged['Year'] = df_merged['Date'].dt.year
df_merged['Month'] = df_merged['Date'].dt.month

# 2. Calculate Unit Price (Revenue divided by Units Sold)
df_merged['UnitPrice'] = df_merged['Revenue'] / df_merged['UnitsSold']

# 3. Basic Outlier Detection using standard deviation rule
rev_mean = df_merged['Revenue'].mean()
rev_std = df_merged['Revenue'].std()
cutoff = rev_std * 3

lower_limit = rev_mean - cutoff
upper_limit = rev_mean + cutoff

# Flag outliers as a boolean column
df_merged['Is_Outlier'] = (df_merged['Revenue'] < lower_limit) | (df_merged['Revenue'] > upper_limit)

print(f"Number of statistical revenue outliers detected: {df_merged['Is_Outlier'].sum()}")
print("\n")

# ==============================================================================
# SECTION 4: DATA AGGREGATION (GROUP BY)
# ==============================================================================
print("--- SECTION 4: CATEGORY PERFORMANCE ---")
# Group data by Product Category to find total revenue and average units sold
category_summary = df_merged.groupby('CategoryName').agg(
    Total_Revenue=('Revenue', 'sum'),
    Average_Units_Sold=('UnitsSold', 'mean'),
    Total_Transactions=('SaleID', 'count')
).reset_index()

# Sort results to see the highest revenue earning category at the top
category_summary = category_summary.sort_values(by='Total_Revenue', ascending=False)
print(category_summary.to_string(index=False))
print("\n")

# ==============================================================================
# SECTION 5: DATA VISUALIZATION
# ==============================================================================
print("--- SECTION 5: GENERATING CHARTS ---")
os.makedirs('fresher_plots', exist_ok=True)

# Chart 1: Bar Chart of Total Revenue by Category
fig, ax = plt.subplots(figsize=(8, 5))
# Note: fixed the hue deprecation warning from original output by assigning x to hue
sns.barplot(data=category_summary, x='CategoryName', y='Total_Revenue', hue='CategoryName', palette='Blues_r', legend=False, ax=ax)
ax.set_title('Total Revenue Contributed by Product Category', weight='bold', pad=15)
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Revenue (₹)')
plt.tight_layout()
plt.savefig('fresher_plots/01_revenue_by_category.png', dpi=100)
plt.close()

# Chart 2: Scatter Plot of Units Sold vs Total Revenue
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_merged, x='UnitsSold', y='Revenue', alpha=0.6, color='#2ec4b6', ax=ax)
ax.set_title('Relationship Between Units Sold and Total Transaction Revenue', weight='bold', pad=15)
ax.set_xlabel('Number of Units Sold')
ax.set_ylabel('Transaction Revenue (₹)')
plt.tight_layout()
plt.savefig('fresher_plots/02_units_vs_revenue.png', dpi=100)
plt.close()

# Chart 3: Monthly Revenue Trend Line
monthly_trend = df_merged.groupby('Month')['Revenue'].sum().reset_index()
fig, ax = plt.subplots(figsize=(9, 5))
sns.lineplot(data=monthly_trend, x='Month', y='Revenue', marker='o', color='crimson', linewidth=2, ax=ax)
ax.set_title('Monthly Revenue Performance Trend', weight='bold', pad=15)
ax.set_xlabel('Month Number')
ax.set_ylabel('Total Revenue Realized (₹)')
ax.set_xticks(range(1, 13))
plt.tight_layout()
plt.savefig('fresher_plots/03_monthly_revenue_trend.png', dpi=100)
plt.close()

print("All charts have been compiled and successfully saved inside the 'fresher_plots/' folder.")
