import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs" / "charts"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_visualizations():
    try:
        df = pd.read_csv(DATA_DIR / "transactions_integrated.csv")
        elasticity_df = pd.read_csv(DATA_DIR / "price_elasticity.csv")
    except FileNotFoundError:
        return

    # Set seaborn style for nicer professional plots
    sns.set_theme(style="whitegrid", palette="muted")

    # 1. AOV comparison
    plt.figure(figsize=(8, 5))
    sns.barplot(x="region", y="order_value_usd", data=df, errorbar=None)
    plt.title("Average Order Value (USD) by Region", fontsize=14, pad=15)
    plt.ylabel("Avg Order Value ($)")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "aov_comparison.png", dpi=300)

    # 2. Spending distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="order_value_usd", hue="region", bins=40, kde=True, element="step")
    plt.title("Order Value Distribution (Outliers Removed)", fontsize=14, pad=15)
    plt.xlabel("Order Value ($)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "spending_distribution.png", dpi=300)
    
    # 3. Price Elasticity: Volume by Price Tier
    plt.figure(figsize=(8, 5))
    sns.barplot(x="price_tier", y="quantity", hue="region", data=elasticity_df)
    plt.title("Price Elasticity: Total Items Sold per Price Tier", fontsize=14, pad=15)
    plt.xlabel("Price Tier")
    plt.ylabel("Total Quantity Sold")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "price_elasticity.png", dpi=300)
    
    # Show all visuals simultaneously
    plt.show()

if __name__ == "__main__":
    create_visualizations()