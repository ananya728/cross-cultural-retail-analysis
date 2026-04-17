import os
import mysql.connector
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

# Import cleaning functions
from data_cleaning import clean_transactions, remove_outliers_iqr

# Load environment variables
load_dotenv()

# Setup paths (cross-os compatibility)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# Currency conversion constants
INR_TO_USD = 0.012
JPY_TO_USD = 0.0067

def run_analysis():
    transactions = pd.read_csv(DATA_RAW / "transactions.csv")
    products = pd.read_csv(DATA_RAW / "products.csv")
    stores = pd.read_csv(DATA_RAW / "stores.csv")

    # 1. Integration (Merging relational datasets)
    # Drop region from products & stores if they exist to avoid column name collisions
    if "region" in products.columns:
        products = products.drop(columns=["region"])
    if "region" in stores.columns:
        stores = stores.drop(columns=["region"])
        
    merged_data = transactions.merge(products, on="product_id", how="left")
    merged_data = merged_data.merge(stores, on="store_id", how="left")

    # 2. Data Cleaning
    cleaned_data = clean_transactions(merged_data)

    # 3. Currency Normalization
    # Price is taken from products table implicitly during merge, or transactions table.
    # The original script used transactions["price"]. Since we merged products, we'll use transactions' price.
    cleaned_data["price_usd"] = np.where(
        cleaned_data["region"] == "India",
        cleaned_data["price_x"] * INR_TO_USD if "price_x" in cleaned_data.columns else cleaned_data["price"] * INR_TO_USD,
        cleaned_data["price_x"] * JPY_TO_USD if "price_x" in cleaned_data.columns else cleaned_data["price"] * JPY_TO_USD
    )

    cleaned_data["order_value_usd"] = cleaned_data["price_usd"] * cleaned_data["quantity"]

    # 4. Outlier Detection
    final_data = remove_outliers_iqr(cleaned_data, "order_value_usd")

    # 5. Average Order Value (AOV)
    aov = final_data.groupby("region")["order_value_usd"].mean().reset_index()
    print("\n--- Average Order Value (AOV) in USD ---")
    print(aov.to_string(index=False))

    # 6. Price Elasticity / Inventory Prep (Quantity sold by price bins)
    # Bin prices into categories: Low, Medium, High
    bins = [0, 20, 50, float('inf')]
    labels = ["Low (<$20)", "Medium ($20-$50)", "High (>$50)"]
    final_data["price_tier"] = pd.cut(final_data["price_usd"], bins=bins, labels=labels)
    
    price_elasticity = final_data.groupby(["region", "price_tier"], observed=True)["quantity"].sum().reset_index()
    print("\n--- Total Items Sold per Price Tier ---")
    print(price_elasticity.to_string(index=False))
    print("") # Empty line for spacing

    # Save processed data for visualization
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    final_data.to_csv(DATA_PROCESSED / "transactions_integrated.csv", index=False)
    price_elasticity.to_csv(DATA_PROCESSED / "price_elasticity.csv", index=False)

    # 7. Database Export
    export_to_db(final_data)

def export_to_db(df: pd.DataFrame):
    """Exports a sample of the processed dataframe into MySQL"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "fashion_retail")
        )
        cursor = conn.cursor()
        
        # In a real pipeline, we'd create tables if they don't exist.
        # Assuming table `transactions` exists but we can recreate it for the new schema.
        cursor.execute("DROP TABLE IF EXISTS analytics_export")
        
        # Simple schema creation
        cursor.execute("""
        CREATE TABLE analytics_export (
            transaction_id INT,
            customer_id INT,
            product_id INT,
            store_id INT,
            quantity INT,
            region VARCHAR(50),
            price_usd FLOAT,
            order_value_usd FLOAT
        )
        """)
        
        # Prepare data for bulk insert (subset of columns to keep it clean)
        cols_to_keep = ["transaction_id", "customer_id", "product_id", "store_id", "quantity", "region", "price_usd", "order_value_usd"]
        insert_data = [tuple(x) for x in df[cols_to_keep].to_numpy()]
        
        sql = """
        INSERT INTO analytics_export (transaction_id, customer_id, product_id, store_id, quantity, region, price_usd, order_value_usd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Use executemany for much faster bulk inserts instead of iterrows!
        cursor.executemany(sql, insert_data)
        conn.commit()
    except Exception:
        pass
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_analysis()