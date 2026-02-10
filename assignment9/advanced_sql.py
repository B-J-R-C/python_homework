import sqlite3
import os

# Define the path to the database
db_path = '../db/lesson.db'

try:
    # 1. Connect to the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 2. Define the SQL Query
        sql_query = """
            SELECT 
                orders.order_id, 
                SUM(products.price * line_items.quantity) AS total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
            ORDER BY orders.order_id
            LIMIT 5;
        """
        
        # 3. Execute the query
        cursor.execute(sql_query)
        
        # 4. Fetch and Print results
        rows = cursor.fetchall()
        
        print("--- Total Price for First 5 Orders ---")
        for row in rows:
            order_id = row[0]
            total_price = row[1]
            print(f"Order ID: {order_id}, Total: ${total_price:.2f}")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"A general error occurred: {e}")