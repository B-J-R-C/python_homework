import sqlite3
import os

db_path = '../db/magazines.db'

# Checkdirectory exists
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# --- Helper Functions ---

def add_publisher(cursor, name):
    cursor.execute("SELECT id FROM publishers WHERE name = ?", (name,))
    if cursor.fetchone():
        return
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f"Added publisher: {name}")
    except sqlite3.Error as e:
        print(f"Error adding publisher {name}: {e}")

def add_magazine(cursor, magazine_name, publisher_name):
    cursor.execute("SELECT id FROM publishers WHERE name = ?", (publisher_name,))
    result = cursor.fetchone()
    if not result:
        return
    publisher_id = result[0]

    cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
    if cursor.fetchone():
        return

    try:
        cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (magazine_name, publisher_id))
        print(f"Added magazine: {magazine_name}")
    except sqlite3.Error as e:
        print(f"Error adding magazine {magazine_name}: {e}")

def add_subscriber(cursor, name, address):
    cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
    if cursor.fetchone():
        return
    try:
        cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        print(f"Added subscriber: {name}")
    except sqlite3.Error as e:
        print(f"Error adding subscriber {name}: {e}")

def add_subscription(cursor, subscriber_name, magazine_name, expiration_date):
    cursor.execute("SELECT id FROM subscribers WHERE name = ?", (subscriber_name,))
    sub_res = cursor.fetchone()
    cursor.execute("SELECT id FROM magazines WHERE name = ?", (magazine_name,))
    mag_res = cursor.fetchone()

    if not sub_res or not mag_res:
        return

    subscriber_id = sub_res[0]
    magazine_id = mag_res[0]

    cursor.execute('''SELECT id FROM subscriptions 
        WHERE subscriber_id = ? AND magazine_id = ?''', (subscriber_id, magazine_id))
    if cursor.fetchone():
        return

    try:
        cursor.execute('''INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) 
            VALUES (?, ?, ?)''', (subscriber_id, magazine_id, expiration_date))
        print(f"Added subscription: {subscriber_name} -> {magazine_name}")
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")

# --- Task 4 Query Function ---

def run_queries(cursor):
    print("\n--- QUERY 1: All Subscribers ---")
    cursor.execute("SELECT * FROM subscribers")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    print("\n--- QUERY 2: Magazines Sorted by Name ---")
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    print("\n--- QUERY 3: Magazines for Publisher 'Condé Nast' (JOIN) ---")
    # Join
    cursor.execute('''
        SELECT magazines.name 
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = 'Condé Nast'
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# --- Main Execution Block ---

try:
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    # 1. Create Tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS publishers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
        publisher_id INTEGER, FOREIGN KEY (publisher_id) REFERENCES publishers(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, subscriber_id INTEGER, magazine_id INTEGER,
        expiration_date TEXT NOT NULL,
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id))''')

    # 2. Populate Data
    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Time Inc.")
    add_publisher(cursor, "National Geographic Partners")
    add_magazine(cursor, "Vogue", "Condé Nast")
    add_magazine(cursor, "Time", "Time Inc.")
    add_magazine(cursor, "National Geographic", "National Geographic Partners")
    add_magazine(cursor, "The New Yorker", "Condé Nast") 
    add_subscriber(cursor, "Alice Johnson", "123 Maple St")
    add_subscriber(cursor, "Bob Smith", "456 Oak Ave")
    add_subscriber(cursor, "Charlie Brown", "789 Pine Ln")
    add_subscription(cursor, "Alice Johnson", "Vogue", "2025-12-31")
    add_subscription(cursor, "Alice Johnson", "Time", "2024-06-30")
    add_subscription(cursor, "Bob Smith", "National Geographic", "2025-01-01")
    add_subscription(cursor, "Charlie Brown", "The New Yorker", "2024-11-15")

    # 3. Commit Changes
    connection.commit()

    # 4. RUN THE QUERIES (Task 4)
    run_queries(cursor)
    
    connection.close()
    print("\nConnection closed.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"A general error occurred: {e}")