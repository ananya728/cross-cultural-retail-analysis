import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

np.random.seed(42)

# -----------------------------
# PARAMETERS
# -----------------------------

NUM_CUSTOMERS = 2000
NUM_PRODUCTS = 300
NUM_TRANSACTIONS = 12000

regions = ["India", "Japan"]

categories = [
    "Shirts","T-Shirts","Jeans","Dresses",
    "Jackets","Shoes","Sneakers","Kurtas",
    "Sweaters","Shorts"
]

brands = [
    "Zara","H&M","Uniqlo","Levis",
    "Nike","Adidas","FabIndia","Muji"
]

# -----------------------------
# CUSTOMERS TABLE
# -----------------------------

customers = []

for i in range(NUM_CUSTOMERS):
    region = random.choice(regions)

    customers.append({
        "customer_id": i+1,
        "name": fake.name(),
        "age": random.randint(18,60),
        "region": region
    })

customers_df = pd.DataFrame(customers)

# -----------------------------
# STORES TABLE
# -----------------------------

stores = [
    {"store_id":1,"city":"Mumbai","region":"India"},
    {"store_id":2,"city":"Delhi","region":"India"},
    {"store_id":3,"city":"Tokyo","region":"Japan"},
    {"store_id":4,"city":"Osaka","region":"Japan"}
]

stores_df = pd.DataFrame(stores)

# -----------------------------
# PRODUCTS TABLE
# -----------------------------

products = []

for i in range(NUM_PRODUCTS):

    region = random.choice(regions)

    if region == "India":
        price = random.randint(500,4000)  # INR
    else:
        price = random.randint(2000,12000)  # JPY

    products.append({
        "product_id": i+1,
        "product_name": random.choice(categories),
        "brand": random.choice(brands),
        "price": price,
        "region": region
    })

products_df = pd.DataFrame(products)

# -----------------------------
# TRANSACTIONS TABLE
# -----------------------------

transactions = []

for i in range(NUM_TRANSACTIONS):

    customer = customers_df.sample(1).iloc[0]

    product = products_df[
        products_df["region"] == customer["region"]
    ].sample(1).iloc[0]

    quantity = random.randint(1,4)

    transactions.append({
        "transaction_id": i+1,
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "store_id": random.choice(stores_df[
            stores_df["region"]==customer["region"]
        ]["store_id"].values),
        "quantity": quantity,
        "price": product["price"],
        "region": customer["region"]
    })

transactions_df = pd.DataFrame(transactions)

# -----------------------------
# SAVE DATA
# -----------------------------

customers_df.to_csv("data/raw/customers.csv",index=False)
stores_df.to_csv("data/raw/stores.csv",index=False)
products_df.to_csv("data/raw/products.csv",index=False)
transactions_df.to_csv("data/raw/transactions.csv",index=False)

print("Dataset generated successfully!")