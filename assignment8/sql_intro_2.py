import sqlite3
import pandas as pd
import os

# 1. Connect to 'lesson.db' database
db_path = '../db/lesson.db'

if not os.path.exists(db_path):
    print(f"ERROR: Could not find database at {db_path}")
    print("Please ensure you have completed the previous lesson that created this file.")
else:
    try:
        connection = sqlite3.connect(db_path)
        print("Connected to lesson.db")

        # 2. SQL Query JOIN
        sql_query = '''
            SELECT 
                line_items.id AS line_item_id, 
                line_items.quantity, 
                products.product_id, 
                products.product_name, 
                products.price 
            FROM line_items 
            JOIN products 
            ON line_items.product_id = products.product_id
        '''

        # Read into DataFrame
        df = pd.read_sql_query(sql_query, connection)
        
        # Close
        connection.close()

        print("\n--- First 5 Rows (Raw Data) ---")
        print(df.head())

        # Add 'total'
        df['total'] = df['quantity'] * df['price']
        
        print("\n--- First 5 Rows (With Total) ---")
        print(df.head())

        # Group by product_id
        summary_df = df.groupby('product_id').agg({
            'line_item_id': 'count',
            'total': 'sum',
            'product_name': 'first'
        })

        # Rename columns so know what
        summary_df = summary_df.rename(columns={'line_item_id': 'order_count', 'total': 'total_sales'})

        # Sort by product_name
        summary_df = summary_df.sort_values('product_name')

        print("\n--- Final Summary (First 5 Rows) ---")
        print(summary_df.head())

        # Write to CSV
        output_file = 'order_summary.csv'
        summary_df.to_csv(output_file)
        print(f"\nSuccessfully wrote summary to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")