# E-Commerce Sales Data Analysis 📊

## Overview
This project demonstrates an end-to-end data analysis workflow using Python. It simulates a real-world analytics scenario by ingesting raw data from separate sources, performing data cleaning, conducting feature engineering, and generating business-ready visualizations.

## Project Structure
* `data_analysis.py` - The main Python script that handles the entire pipeline.
* `sales_data.csv` - Synthetic transactional dataset containing sale IDs, products, units sold, and revenue.
* `products_data.csv` - Lookup dataset containing product names and their respective categories.
* `fresher_plots/` - Directory where generated visualizations are automatically saved.

## Tech Stack
* **Language:** Python 3
* **Libraries:** Pandas, NumPy, Matplotlib, Seaborn

## Key Features & Pipeline Steps
1. **Data Loading & Merging:** Reads raw CSV files and executes an inner merge on `ProductID` to combine transaction records with product metadata.
2. **Data Cleaning:** Implements mean imputation to handle missing revenue values (5% missing data simulation) and drops exact duplicate records.
3. **Feature Engineering:** Extracts date parts (Year, Month), calculates individual `UnitPrice`, and flags statistical revenue outliers using a 3-standard-deviation rule.
4. **Data Aggregation:** Summarizes category-level performance metrics (Total Revenue, Average Units Sold, Total Transactions).
5. **Data Visualization:** Automatically compiles and exports professional charts:
   * Bar Chart: Total Revenue by Product Category
   * Scatter Plot: Relationship between Units Sold and Transaction Revenue
   * Line Chart: Monthly Revenue Performance Trend
