import sqlite3
import os

db_path = '../db/lesson.db'

print(f"Connecting to: {os.path.abspath(db_path)}")

try:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # --- TASK 1: Total Price per Order ---
        print("\n--- Task 1: Total Price for First 5 Orders ---")
        sql_query_1 = """
            SELECT 
                orders.order_id, 
                SUM(products.price * line_items.quantity) 
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
            ORDER BY orders.order_id
            LIMIT 5;
        """
        cursor.execute(sql_query_1)
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"Order ID: {row[0]}, Total: ${row[1]:.2f}")

        # TASK 2: Average Order Price per Customer
        print("\n--- Task 2: Average Order Price per Customer ---")
        
        
        sql_query_2 = """
            SELECT 
                customers.customer_name, 
                AVG(subquery.order_total) 
            FROM customers
            JOIN (
                SELECT 
                    orders.customer_id,
                    SUM(products.price * line_items.quantity) AS order_total
                FROM orders
                JOIN line_items ON orders.order_id = line_items.order_id
                JOIN products ON line_items.product_id = products.product_id
                GROUP BY orders.order_id
            ) AS subquery 
            ON customers.customer_id = subquery.customer_id
            GROUP BY customers.customer_id;
        """
        
        cursor.execute(sql_query_2)
        rows = cursor.fetchall()
        
        if not rows:
            print("No data returned for Task 2.")
        
        for row in rows:
            # Debug raw data if names missing
            # print(f"DEBUG: {row}") 
            
            name = row[0]
            avg_price = row[1]
            
            if name is None:
                name = "Unknown Customer"
            
            if avg_price is None:
                print(f"Customer: {name}, Avg Order Price: $0.00")
            else:
                print(f"Customer: {name}, Avg Order Price: ${avg_price:.2f}")

except sqlite3.Error as e:
    print(f"SQLite Error: {e}")
except Exception as e:
    print(f"General Error: {e}")

