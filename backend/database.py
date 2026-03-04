import sqlite3

def create_connection():
    conn = sqlite3.connect("sales.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            city TEXT,
            product TEXT,
            price INTEGER,
            quantity INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def insert_sample_data():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO sales (date, city, product, price, quantity)
            VALUES 
            ('2025-01-01', 'Delhi', 'ProductA', 100, 50),
            ('2025-01-02', 'Jaipur', 'ProductB', 200, 30)
        """)

    conn.commit()
    conn.close()