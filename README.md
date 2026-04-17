
# Cross-Cultural Fashion Retail Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)

## Project Overview

- **Tools & technologies:** Python (Pandas, Matplotlib, Seaborn), SQL.
- Conducted a comparative analysis of **Indian and Japanese fashion retail markets** to uncover regional consumer behavior patterns.
- Cleaned and integrated **10K+ transactional records** across relational datasets including transactions, stores, and products.
- Applied **currency normalization** and **outlier detection (IQR method)** to compare Average Order Value (AOV) across regions.
- Visualized spending patterns and identified differences in **price elasticity** for regional inventory optimization.

## Data Pipeline Architecture

1. **Data Generation** (`src/generate_data.py`): Generates synthetic relational data mimicking real-world global retail systems (`transactions`, `customers`, `products`, `stores`).
2. **Data Integration & Cleaning** (`src/analysis.py` / `src/data_cleaning.py`): Merges tables to form a comprehensive analytical view. Discards nulls/duplicates and bounds extreme outliers using Interquartile Range (IQR).
3. **Analytics** (`src/analysis.py`): Normalizes currencies (INR/JPY -> USD), calculating Average Order Value (AOV) and generating volume metrics grouped by price tiers to measure elasticity.
4. **Database Export**: Automates bulk uploading cleaned analytics tables into a MySQL database for further downstream business BI querying.
5. **Visualization** (`src/visualization.py`): Generates programmatic Seaborn charts for business stakeholders.

## How to Run the Project

### 1. Environment Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Database Configuration
Copy the `.env.example` file to create a `.env` file in the root directory. Update it with your local MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=fashion_retail
```

### 3. Execution
Run the entire analytical pipeline with a single command:
```bash
python main.py
```
This will automatically:
1. Generate the synthetic data into `data/raw`.
2. Clean, merge, and analyze the data, exporting to `data/processed`.
3. Upload the final analytics payload to your MySQL database.
4. Generate analytical dashboards in `outputs/charts`.

## Final Output
Check the `outputs/charts/` directory to view insights demonstrating AOV comparison, spending distribution, and price elasticity trends between regions.

