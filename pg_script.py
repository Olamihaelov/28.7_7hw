# pip install psycopg2-binary

import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='admin',
        host='localhost',
        port='5432',
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    print("Connected successfully.")
except psycopg2.Error as e:
    print("Connection error:", e)

# Create the users table if it doesn't exist
try:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)
    conn.commit()
    print("Table 'users' created or already exists.")
except psycopg2.Error as e:
    print("Table creation error:", e)
finally:
    cur.close()

# Create the products table for the Streamlit app
try:
    cur = conn.cursor()
    # Drop and recreate the table to ensure clean data
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute("""
        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price NUMERIC(6, 2) NOT NULL,
            in_stock BOOLEAN DEFAULT TRUE
        );
    """)
    conn.commit()
    print("Table 'products' created.")
except psycopg2.Error as e:
    print("Products table creation error:", e)
    conn.rollback()
finally:
    cur.close()

# Insert the exact sample products you specified
try:
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (name, price, in_stock) VALUES
        ('Laptop', 3200.50, TRUE),
        ('Mouse', 99.99, TRUE),
        ('Keyboard', 250.00, FALSE),
        ('Monitor', 1190.95, TRUE);
    """)
    conn.commit()
    print("Sample products inserted.")
except psycopg2.Error as e:
    print("Products insert error:", e)
    conn.rollback()  # Roll back the transaction on error
finally:
    cur.close()

try:
    cur = conn.cursor()
    # Use INSERT ... ON CONFLICT to avoid duplicate key errors
    cur.execute("""
        INSERT INTO users (name, email) VALUES (%s, %s)
        ON CONFLICT (email) DO NOTHING
    """, ("Alice", "alice@example.com"))
    conn.commit()
    print("Data inserted.")
except psycopg2.Error as e:
    print("Insert error:", e)
    conn.rollback()  # Roll back the transaction on error
finally:
    cur.close()


try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        print(row)
except psycopg2.Error as e:
    print("Select error:", e)
    conn.rollback()  # Roll back the transaction on error
finally:
    cur.close()


conn.close()
print("Connection closed.")
