import pandas as pd
import psycopg2
from datetime import datetime
import os
import logging

logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'bakery_db'
DB_USER = 'postgres'
DB_PASSWORD = 'your_password_here'
CSV_FOLDER = r'C:\Users\User\Desktop\Bakery Dashboard\bakery_data'

print("=" * 60)
print("BAKERY DASHBOARD - ETL PROCESS STARTED")
print("=" * 60)
logging.info("=== ETL Process Started ===")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print(f"✅ Connected to database: {DB_NAME}")

    # LOAD PRODUCTS
    print("\n" + "=" * 60)
    print("Loading PRODUCTS...")
    print("=" * 60)
    try:
        products_df = pd.read_csv(os.path.join(CSV_FOLDER, 'PRODUCTS.csv'), skipinitialspace=True)
        cursor.execute('DELETE FROM products;')
        
        for _, row in products_df.iterrows():
            cursor.execute(
                '''INSERT INTO products 
                   (product_id, product_name, category, cost_per_unit, selling_price, shelf_life_hours, daily_capacity)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (row['product_id'], row['product_name'], row['category'],
                 float(row['cost_per_unit']), float(row['selling_price']),
                 int(row['shelf_life_hours']), int(row['daily_capacity']))
            )
        
        conn.commit()
        print(f"✅ Loaded {len(products_df)} products")
    except Exception as e:
        print(f"❌ Error loading products: {e}")
        conn.rollback()

    # LOAD CUSTOMERS
    print("\n" + "=" * 60)
    print("Loading CUSTOMERS...")
    print("=" * 60)
    try:
        customers_df = pd.read_csv(os.path.join(CSV_FOLDER, 'CUSTOMERS.csv'), skipinitialspace=True)
        cursor.execute('DELETE FROM customers;')
        
        for _, row in customers_df.iterrows():
            cursor.execute(
                '''INSERT INTO customers 
                   (customer_id, customer_name, email, phone, city, signup_date, customer_source)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (row['customer_id'], row['customer_name'], row['email'],
                 row['phone'], row['city'], row['signup_date'], row['customer_source'])
            )
        
        conn.commit()
        print(f"✅ Loaded {len(customers_df)} customers")
    except Exception as e:
        print(f"❌ Error loading customers: {e}")
        conn.rollback()

    # LOAD ORDERS
    print("\n" + "=" * 60)
    print("Loading ORDERS...")
    print("=" * 60)
    try:
        orders_df = pd.read_csv(os.path.join(CSV_FOLDER, 'ORDERS.csv'), skipinitialspace=True)
        cursor.execute('DELETE FROM orders;')
        
        for _, row in orders_df.iterrows():
            cursor.execute(
                '''INSERT INTO orders 
                   (order_id, customer_id, order_date, order_time, total_amount, delivery_fee, discount, order_status, delivery_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (row['order_id'], row['customer_id'], row['order_date'], row['order_time'],
                 float(row['total_amount']), float(row['delivery_fee']), float(row['discount']),
                 row['order_status'], row['delivery_date'])
            )
        
        conn.commit()
        print(f"✅ Loaded {len(orders_df)} orders")
    except Exception as e:
        print(f"❌ Error loading orders: {e}")
        conn.rollback()

    # LOAD ORDER_ITEMS
    print("\n" + "=" * 60)
    print("Loading ORDER_ITEMS...")
    print("=" * 60)
    try:
        order_items_df = pd.read_csv(os.path.join(CSV_FOLDER, 'ORDER_ITEMS.csv'), skipinitialspace=True)
        cursor.execute('DELETE FROM order_items;')
        
        for _, row in order_items_df.iterrows():
            cursor.execute(
                '''INSERT INTO order_items 
                   (order_item_id, order_id, product_id, quantity, unit_price, line_total)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (row['order_item_id'], row['order_id'], row['product_id'],
                 int(row['quantity']), float(row['unit_price']), float(row['line_total']))
            )
        
        conn.commit()
        print(f"✅ Loaded {len(order_items_df)} order items")
    except Exception as e:
        print(f"❌ Error loading order_items: {e}")
        conn.rollback()

    # LOAD INVENTORY
    print("\n" + "=" * 60)
    print("Loading INVENTORY...")
    print("=" * 60)
    try:
        inventory_df = pd.read_csv(os.path.join(CSV_FOLDER, 'INVENTORY.csv'), skipinitialspace=True)
        cursor.execute('DELETE FROM inventory;')
        
        for _, row in inventory_df.iterrows():
            cursor.execute(
                '''INSERT INTO inventory 
                   (inventory_id, product_id, date, quantity_available, quantity_sold, quantity_wasted, restock_date)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (row['inventory_id'], row['product_id'], row['date'],
                 int(row['quantity_available']), int(row['quantity_sold']),
                 int(row['quantity_wasted']), row['restock_date'])
            )
        
        conn.commit()
        print(f"✅ Loaded {len(inventory_df)} inventory records")
    except Exception as e:
        print(f"❌ Error loading inventory: {e}")
        conn.rollback()

    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ ETL PROCESS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n🎉 All data loaded!")

except Exception as e:
    print(f"\n❌ Fatal error: {e}")