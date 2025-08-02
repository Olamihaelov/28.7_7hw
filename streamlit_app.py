import streamlit as st
import psycopg2
from psycopg2 import extras

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# Section A: Calculator UI
st.title("👤 Name: Oly | Project: 28.7")

num1 = st.text_input("Number 1", "5")
num2 = st.text_input("Number 2", "8")

if st.button("Add"):
    sum = int(num1) + int(num2)
    st.success(f"✅ Sum: {sum}")

# Section B: Show Available Products
st.subheader("📦 Available Products")

if st.button("Show Products"):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Select With Condition
        cursor.execute("SELECT * FROM products WHERE in_stock = TRUE;")
        rows = cursor.fetchall()

        # Show the result
        for row in rows:
            st.write(dict(row))

    except psycopg2.Error as e:
        st.error(f"Database error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
