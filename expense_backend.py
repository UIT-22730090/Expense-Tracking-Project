import sqlite3
import pandas as pd

DATABASE = 'expense_manager.db'

def create_tables():
    """Create necessary tables if they do not exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            birthday DATE NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date DATE NOT NULL,
            transaction_type TEXT NOT NULL,
            group_name TEXT NOT NULL,
            transaction_name TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            username TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL,  -- 'Thu nhập' or 'Chi tiêu'
            group_name TEXT NOT NULL  -- 'Gia đình', 'Cá nhân', etc.
        )
    ''')
    conn.commit()
    conn.close()

def login(username, password):
    """Check if the user exists with the provided username and password."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_transactions(transaction_date, transaction_type, group_name, transaction_name, amount, note, username):
    """Add a transaction to the database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (transaction_date, transaction_type, group_name, transaction_name, amount, note, username)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_date, transaction_type, group_name, transaction_name, amount, note, username))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_summary(username):
    """Retrieve a summary of income and expenses."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type = 'Thu nhập' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN transaction_type = 'Chi tiêu' THEN amount ELSE 0 END) AS total_expense
        FROM transactions
        WHERE username = ?
    """, (username,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_transactions(username):
    """Retrieve all transactions for the given username."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaction_date, transaction_type, group_name, transaction_name, amount, note
        FROM transactions
        WHERE username = ?
    """, (username,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def search_transactions(transaction_name=None, transaction_type="All", group_name="All", date_range="All"):
    """Search transactions based on filters: transaction name, transaction type, group name, and date range."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Base query
    query = """
        SELECT transaction_date, transaction_type, group_name, transaction_name, amount, note
        FROM transactions
        WHERE 1=1
    """
    params = []

    # Filter by transaction name if provided
    if transaction_name:
        query += " AND transaction_name LIKE ?"
        params.append(f"%{transaction_name}%")

    # Filter by date range if provided
    if date_range != "All":
        if date_range == "Today":
            query += " AND DATE(transaction_date) = DATE('now')"
        elif date_range == "Last 7 Days":
            query += " AND DATE(transaction_date) >= DATE('now', '-7 days')"
        elif date_range == "Last 30 Days":
            query += " AND DATE(transaction_date) >= DATE('now', '-30 days')"

    # Filter by transaction type if not 'All'
    if transaction_type != "All":
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    # Filter by group name if not 'All'
    if group_name != "All":
        query += " AND group_name = ?"
        params.append(group_name)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_unique_values(column_name):
    """Fetch unique values for a given column from the transactions table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT DISTINCT {column_name} FROM transactions"
    cursor.execute(query)
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_personal_info(username):
    """Retrieve personal information for the given username."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT full_name, birthday, email, phone_number
        FROM users
        WHERE username = ?
    """, (username,))
    info = cursor.fetchone()
    conn.close()
    return dict(zip(['full_name', 'birthday', 'email', 'phone_number'], info))

def get_options_from_db(query):
    """Get options from the database for dropdowns."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    options = [row[0] for row in cursor.fetchall()]
    conn.close()
    return options

def get_data(query):
    """Retrieve data based on the provided SQL query."""
    conn = sqlite3.connect(DATABASE)  # Replace DATABASE with your actual database path
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data