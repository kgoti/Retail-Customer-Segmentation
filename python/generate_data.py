"""
Retail Customer Segmentation Dataset Generator
Generates realistic e-commerce transaction data for RFM analysis
"""

import csv, random, math
from datetime import datetime, timedelta

random.seed(77)

COUNTRIES  = ["Germany","Germany","Germany","Austria","Switzerland","Germany","Germany"]
CATEGORIES = ["Electronics","Clothing","Home & Garden","Sports","Books","Beauty","Food & Drink","Toys"]
PRODUCTS   = {
    "Electronics":  [("Laptop Stand",49.99),("USB Hub",29.99),("Webcam",79.99),("Headphones",149.99),("Mouse",39.99)],
    "Clothing":     [("T-Shirt",19.99),("Jeans",59.99),("Jacket",89.99),("Sneakers",79.99),("Dress",49.99)],
    "Home & Garden":[("Candle Set",24.99),("Plant Pot",14.99),("Cushion",34.99),("Lamp",69.99),("Rug",129.99)],
    "Sports":       [("Yoga Mat",39.99),("Water Bottle",19.99),("Resistance Band",14.99),("Dumbbells",59.99),("Skipping Rope",9.99)],
    "Books":        [("Python Cookbook",34.99),("Data Science Guide",44.99),("Novel",12.99),("Cookbook",24.99),("Travel Guide",16.99)],
    "Beauty":       [("Face Cream",39.99),("Shampoo",14.99),("Perfume",79.99),("Lip Balm",8.99),("Serum",54.99)],
    "Food & Drink": [("Coffee Beans",19.99),("Tea Collection",24.99),("Protein Bar",2.99),("Nuts Mix",12.99),("Olive Oil",16.99)],
    "Toys":         [("LEGO Set",49.99),("Puzzle",19.99),("Board Game",34.99),("Stuffed Animal",19.99),("Art Kit",24.99)],
}
CHANNELS = ["Website","Mobile App","Website","Website","Email Campaign","Mobile App"]

analysis_date = datetime(2024, 1, 1)

# ── 1. customers.csv ─────────────────────────────────────────────────────────
customers = []
for i in range(1, 1001):
    reg = analysis_date - timedelta(days=random.randint(30, 1095))
    customers.append([f"C{i:04d}", reg.strftime("%Y-%m-%d"), random.choice(COUNTRIES), random.choice(CHANNELS)])

with open("/home/claude/projects/3_retail_segmentation/data/customers.csv", "w", newline="") as f:
    csv.writer(f).writerows([["customer_id","registration_date","country","acquisition_channel"]] + customers)
print(f"customers.csv → {len(customers)} rows")

# ── 2. orders.csv ────────────────────────────────────────────────────────────
orders = []
order_id = 1
# Give different customers different purchasing patterns (for realistic RFM spread)
for cust in customers:
    cid         = cust[0]
    cust_reg    = datetime.strptime(cust[1], "%Y-%m-%d")
    days_active = (analysis_date - cust_reg).days
    num_orders  = max(1, int(random.gauss(5, 4)))  # avg 5 orders
    for _ in range(num_orders):
        order_date = cust_reg + timedelta(days=random.randint(0, days_active))
        if order_date >= analysis_date:
            continue
        cat     = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[cat])
        qty     = random.randint(1, 5)
        price   = product[1]
        disc    = random.choice([0, 0, 0, 5, 10, 15, 20])
        total   = round(qty * price * (1 - disc / 100), 2)
        orders.append([
            f"O{order_id:06d}", cid, order_date.strftime("%Y-%m-%d"),
            cat, product[0], qty, price, disc, total,
            "Delivered" if random.random() > 0.05 else "Returned"
        ])
        order_id += 1

with open("/home/claude/projects/3_retail_segmentation/data/orders.csv", "w", newline="") as f:
    csv.writer(f).writerows([["order_id","customer_id","order_date","category","product","quantity","unit_price","discount_pct","total_amount","status"]] + orders)
print(f"orders.csv → {len(orders)} rows")
print("All datasets generated.")
