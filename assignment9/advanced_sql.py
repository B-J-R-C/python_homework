import sqlite3
import os

db_path = '../db/lesson.db'

print(f"Connecting to: {os.path.abspath(db_path)}")

try:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1") 
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

        # --- TASK 2: Average Order Price per Customer ---
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
        for row in rows:
            name = row[0]
            avg_price = row[1]
            if name and avg_price:
                print(f"Customer: {name}, Avg Order Price: ${avg_price:.2f}")

        # --- TASK 3: Insert Transaction ---
        print("\n--- Task 3: Insert Transaction (New Order) ---")

        # 1. Get Customer ID
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
        cust_res = cursor.fetchone()
        
        if not cust_res:
            print("Error: Customer 'Perez and Sons' not found.")
        else:
            customer_id = cust_res[0]

            # 2. Get Employee ID
            cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
            emp_res = cursor.fetchone()
            
            if not emp_res:
                print("Error: Employee 'Miranda Harris' not found.")
            else:
                employee_id = emp_res[0]

                # 3. Get 5 Cheapest Products
                cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
                products = cursor.fetchall()

                # 4. Insert Order (Using 'date' column)
                cursor.execute("INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, DATE('now')) RETURNING order_id", 
                               (customer_id, employee_id))
                
                new_order_id = cursor.fetchone()[0]
                print(f"Created New Order ID: {new_order_id}")

                # 5. Insert Line Items
                for prod in products:
                    product_id = prod[0]
                    cursor.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, 10)", 
                                   (new_order_id, product_id))
                
                print("Inserted 5 line items.")

                # 6. Verify Output
                print(f"\n--- Verification: Items in Order {new_order_id} ---")
                
                # CHANGED: line_items.id -> line_items.line_item_id
                verify_sql = """
                    SELECT line_items.line_item_id, line_items.quantity, products.product_name 
                    FROM line_items 
                    JOIN products ON line_items.product_id = products.product_id 
                    WHERE line_items.order_id = ?
                """
                cursor.execute(verify_sql, (new_order_id,))
                items = cursor.fetchall()
                for item in items:
                    print(f"Line Item: {item[0]}, Qty: {item[1]}, Product: {item[2]}")

except sqlite3.Error as e:
    # This will print available columns if there is still an error, helping you debug
    print(f"SQLite Error: {e}")
    if "no such column" in str(e):
        print("Existing columns in line_items table:")
        # Create a new cursor to avoid transaction issues
        try:
            temp_cursor = conn.cursor()
            temp_cursor.execute("PRAGMA table_info(line_items)")
            columns = [col[1] for col in temp_cursor.fetchall()]
            print(columns)
        except:
            pass

except Exception as e:
    print(f"General Error: {e}")