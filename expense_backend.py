import sqlite3
import pandas as pd
from tkinter import messagebox

#create_table
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
            phone_number TEXT NOT NULL UNIQUE,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
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
    
    cursor.execute('''
                INSERT OR IGNORE INTO transaction_types (type_name, group_name) 
                VALUES 
                ('Chi tiêu', 'Cá nhân'),
                ('Chi tiêu', 'Gia đình'),
                ('Chi tiêu', 'Sức khỏe'),
                ('Chi tiêu', 'Phương tiện'),
                ('Chi tiêu', 'Đầu tư'),
                ('Chi tiêu', 'Học tập'),
                ('Chi tiêu', 'Giải trí'),
                ('Chi tiêu', 'Ăn uống'),
                ('Chi tiêu', 'Nhà cửa'),
                ('Chi tiêu', 'Du lịch'),
                ('Chi tiêu', 'Mua sắm'),
                ('Chi tiêu', 'Y tế'),
                ('Chi tiêu', 'Dịch vụ'),
                ('Chi tiêu', 'Trợ cấp'),
                ('Chi tiêu', 'Hóa đơn'),
                ('Chi tiêu', 'Giao thông'),
                ('Chi tiêu', 'Bảo hiểm'),
                ('Chi tiêu', 'Thực phẩm'),
                ('Chi tiêu', 'Giáo dục'),
                ('Chi tiêu', 'Văn phòng phẩm'),
                ('Chi tiêu', 'Thể thao'),
                ('Chi tiêu', 'Từ thiện'),
                ('Chi tiêu', 'Tiêu dùng khác'),
                ('Thu nhập', 'Lương'),
                ('Thu nhập', 'Trợ cấp'),
                ('Thu nhập', 'Đầu tư'),
                ('Thu nhập', 'Tiền thưởng'),
                ('Thu nhập', 'Kinh doanh'),
                ('Thu nhập', 'Chuyển nhượng'),
                ('Thu nhập', 'Tiền cho thuê'),
                ('Thu nhập', 'Lãi suất ngân hàng'),
                ('Thu nhập', 'Cổ tức'),
                ('Thu nhập', 'Quà tặng'),
                ('Thu nhập', 'Tiền thừa kế'),
                ('Thu nhập', 'Tiền bán tài sản'),
                ('Thu nhập', 'Chia sẻ lợi nhuận'),
                ('Thu nhập', 'Kinh doanh online'),
                ('Thu nhập', 'Thù lao'),
                ('Thu nhập', 'Học bổng'),
                ('Thu nhập', 'Doanh thu'),
                ('Thu nhập', 'Tiền thưởng khác'),
                ('Thu nhập', 'Tiền từ hợp tác'),
                ('Thu nhập', 'Doanh thu khác')
                ''')
    conn.commit()
    conn.close()

def register_user(full_name, username, password, re_password, birthday, email, phone_number, security_question, security_answer):
    """Insert a new user into the database with password confirmation and error handling."""
    
    # Ensure password confirmation matches
    if password != re_password:
        messagebox.showerror("Error", "Passwords do not match. Please re-enter your password.")
        return False
    
    # Check if any fields are empty
    if not all([full_name, username, password, re_password, birthday, email, phone_number, security_question, security_answer]):
        messagebox.showerror("Error", "All fields must be filled out.")
        return False

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (full_name, username, password, birthday, email, phone_number, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, username, password, birthday, email, phone_number, security_question, security_answer))
        conn.commit()
        conn.close()
        
        # Show success message
        messagebox.showinfo("Success", "Registration successful!")
        return True  # Indicate success
    
    # Handle database-specific errors (like unique constraint violations)
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror("Error", "Username, email, or phone number already exists. Please choose different values.")
        else:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return False
    
    # Handle any other errors
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return False

def add_sample_transaction(username):
    """Add a sample transaction to the database with the provided username."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"""
                INSERT OR IGNORE INTO transactions (transaction_date, transaction_type, group_name, transaction_name, amount, note, username)
                VALUES
                ('2024-01-03', 'Chi tiêu', 'Cá nhân', 'Mua sách', 80000.00, 'Mua sách mới', '{username}'),
                ('2024-01-07', 'Thu nhập', 'Lương', 'Lương tháng 1', 5000000.00, 'Lương tháng 1', '{username}'),
                ('2024-01-15', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 250000.00, 'Chi phí ăn uống', '{username}'),
                ('2024-01-20', 'Chi tiêu', 'Sức khỏe', 'Thuốc', 75000.00, 'Chi phí thuốc men', '{username}'),
                ('2024-01-25', 'Thu nhập', 'Kinh doanh', 'Doanh thu tháng 1', 2000000.00, 'Doanh thu từ kinh doanh', '{username}'),
                ('2024-01-30', 'Chi tiêu', 'Đầu tư', 'Mua cổ phiếu', 300000.00, 'Đầu tư cổ phiếu', '{username}'),
                ('2024-02-05', 'Chi tiêu', 'Học tập', 'Khóa học trực tuyến', 120000.00, 'Chi phí học tập', '{username}'),
                ('2024-02-10', 'Thu nhập', 'Lãi suất ngân hàng', 'Lãi suất tháng 2', 150000.00, 'Lãi suất từ ngân hàng', '{username}'),
                ('2024-02-15', 'Chi tiêu', 'Giải trí', 'Đi xem phim', 100000.00, 'Chi phí giải trí', '{username}'),
                ('2024-02-20', 'Chi tiêu', 'Ăn uống', 'Nhà hàng', 200000.00, 'Chi phí ăn nhà hàng', '{username}'),
                ('2024-02-25', 'Chi tiêu', 'Nhà cửa', 'Tiền thuê nhà', 2500000.00, 'Tiền thuê nhà tháng 2', '{username}'),
                ('2024-03-01', 'Thu nhập', 'Lương', 'Lương tháng 3', 5100000.00, 'Lương tháng 3', '{username}'),
                ('2024-03-08', 'Chi tiêu', 'Du lịch', 'Chuyến đi Đà Lạt', 3000000.00, 'Chi phí du lịch', '{username}'),
                ('2024-03-15', 'Chi tiêu', 'Mua sắm', 'Quần áo', 150000.00, 'Mua quần áo mới', '{username}'),
                ('2024-03-20', 'Chi tiêu', 'Y tế', 'Khám bệnh', 120000.00, 'Khám sức khỏe định kỳ', '{username}'),
                ('2024-03-25', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 3', 500000.00, 'Thu nhập từ cổ tức', '{username}'),
                ('2024-04-02', 'Chi tiêu', 'Dịch vụ', 'Cắt tóc', 60000.00, 'Chi phí cắt tóc', '{username}'),
                ('2024-04-07', 'Thu nhập', 'Tiền thưởng', 'Thưởng quý 1', 1200000.00, 'Thưởng công việc', '{username}'),
                ('2024-04-10', 'Chi tiêu', 'Trợ cấp', 'Trợ cấp cho cha mẹ', 300000.00, 'Hỗ trợ cha mẹ', '{username}'),
                ('2024-04-15', 'Chi tiêu', 'Hóa đơn', 'Tiền điện', 400000.00, 'Hóa đơn tiền điện tháng 4', '{username}'),
                ('2024-04-20', 'Chi tiêu', 'Giao thông', 'Xăng xe', 180000.00, 'Chi phí xăng xe', '{username}'),
                ('2024-04-25', 'Thu nhập', 'Tiền bán tài sản', 'Bán xe máy cũ', 3500000.00, 'Bán xe cũ', '{username}'),
                ('2024-05-01', 'Thu nhập', 'Lương', 'Lương tháng 5', 5200000.00, 'Lương tháng 5', '{username}'),
                ('2024-05-05', 'Chi tiêu', 'Bảo hiểm', 'Bảo hiểm y tế', 500000.00, 'Chi phí bảo hiểm', '{username}'),
                ('2024-05-12', 'Chi tiêu', 'Thực phẩm', 'Mua thực phẩm', 220000.00, 'Chi phí thực phẩm', '{username}'),
                ('2024-05-18', 'Thu nhập', 'Quà tặng', 'Nhận quà sinh nhật', 200000.00, 'Quà sinh nhật', '{username}'),
                ('2024-05-23', 'Chi tiêu', 'Giáo dục', 'Đóng học phí', 1500000.00, 'Chi phí học phí', '{username}'),
                ('2024-05-28', 'Chi tiêu', 'Văn phòng phẩm', 'Mua bút viết', 30000.00, 'Chi phí văn phòng phẩm', '{username}'),
                ('2024-06-01', 'Thu nhập', 'Lương', 'Lương tháng 6', 5300000.00, 'Lương tháng 6', '{username}'),
                ('2024-06-08', 'Chi tiêu', 'Thể thao', 'Mua đồ tập gym', 400000.00, 'Chi phí thể thao', '{username}'),
                ('2024-06-12', 'Chi tiêu', 'Từ thiện', 'Quyên góp từ thiện', 200000.00, 'Hoạt động từ thiện', '{username}'),
                ('2024-06-18', 'Chi tiêu', 'Tiêu dùng khác', 'Chi phí linh tinh', 100000.00, 'Chi phí không dự kiến', '{username}'),
                ('2024-06-25', 'Thu nhập', 'Tiền từ hợp tác', 'Doanh thu từ hợp tác', 1000000.00, 'Doanh thu hợp tác', '{username}'),
                ('2024-07-02', 'Chi tiêu', 'Cá nhân', 'Mua điện thoại mới', 2000000.00, 'Chi phí mua điện thoại', '{username}'),
                ('2024-07-06', 'Thu nhập', 'Đầu tư', 'Thu nhập đầu tư', 600000.00, 'Thu nhập từ đầu tư', '{username}'),
                ('2024-07-12', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 250000.00, 'Chi phí ăn uống', '{username}'),
                ('2024-07-18', 'Chi tiêu', 'Sức khỏe', 'Bảo hiểm sức khỏe', 250000.00, 'Bảo hiểm sức khỏe', '{username}'),
                ('2024-07-22', 'Chi tiêu', 'Phương tiện', 'Sửa xe máy', 350000.00, 'Chi phí sửa xe', '{username}'),
                ('2024-07-28', 'Thu nhập', 'Thù lao', 'Thù lao dự án', 800000.00, 'Thù lao công việc', '{username}'),
                ('2024-08-01', 'Thu nhập', 'Lương', 'Lương tháng 8', 5400000.00, 'Lương tháng 8', '{username}'),
                ('2024-08-06', 'Chi tiêu', 'Học tập', 'Mua sách học tập', 70000.00, 'Chi phí mua sách', '{username}'),
                ('2024-08-10', 'Chi tiêu', 'Giải trí', 'Mua game', 300000.00, 'Chi phí giải trí', '{username}'),
                ('2024-08-15', 'Chi tiêu', 'Ăn uống', 'Nhà hàng Nhật', 500000.00, 'Chi phí nhà hàng', '{username}'),
                ('2024-08-20', 'Chi tiêu', 'Nhà cửa', 'Sửa nhà', 1000000.00, 'Chi phí sửa nhà', '{username}'),
                ('2024-08-25', 'Thu nhập', 'Doanh thu khác', 'Doanh thu tháng 8', 1500000.00, 'Doanh thu khác', '{username}'),
                ('2024-09-01', 'Thu nhập', 'Lương', 'Lương tháng 9', 5500000.00, 'Lương tháng 9', '{username}'),
                ('2024-09-05', 'Chi tiêu', 'Du lịch', 'Du lịch Nha Trang', 4000000.00, 'Chi phí du lịch', '{username}'),
                ('2024-09-12', 'Chi tiêu', 'Mua sắm', 'Mua đồ dùng gia đình', 200000.00, 'Chi phí mua sắm', '{username}'),
                ('2024-09-18', 'Chi tiêu', 'Y tế', 'Thuốc bổ', 80000.00, 'Chi phí thuốc bổ', '{username}'),
                ('2024-09-23', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 9', 700000.00, 'Thu nhập từ cổ tức', '{username}'),
                ('2024-10-02', 'Chi tiêu', 'Dịch vụ', 'Cắt cỏ sân vườn', 120000.00, 'Chi phí cắt cỏ', '{username}'),
                ('2024-10-07', 'Thu nhập', 'Tiền thưởng', 'Thưởng quý 3', 1300000.00, 'Thưởng công việc', '{username}'),
                ('2024-10-10', 'Chi tiêu', 'Trợ cấp', 'Trợ cấp cho người thân', 400000.00, 'Hỗ trợ người thân', '{username}'),
                ('2024-10-15', 'Chi tiêu', 'Hóa đơn', 'Tiền nước', 300000.00, 'Hóa đơn tiền nước', '{username}'),
                ('2024-10-20', 'Chi tiêu', 'Giao thông', 'Vé xe buýt', 50000.00, 'Chi phí giao thông', '{username}'),
                ('2024-10-25', 'Thu nhập', 'Tiền bán tài sản', 'Bán điện thoại cũ', 500000.00, 'Bán điện thoại cũ', '{username}'),
                ('2024-11-01', 'Thu nhập', 'Lương', 'Lương tháng 11', 5600000.00, 'Lương tháng 11', '{username}'),
                ('2024-11-05', 'Chi tiêu', 'Bảo hiểm', 'Bảo hiểm xe', 700000.00, 'Chi phí bảo hiểm xe', '{username}'),
                ('2024-11-10', 'Chi tiêu', 'Thực phẩm', 'Mua rau củ', 50000.00, 'Chi phí thực phẩm', '{username}'),
                ('2024-11-15', 'Thu nhập', 'Quà tặng', 'Quà sinh nhật từ bạn', 100000.00, 'Quà sinh nhật', '{username}'),
                ('2024-11-20', 'Chi tiêu', 'Giáo dục', 'Sách giáo khoa', 150000.00, 'Chi phí giáo dục', '{username}'),
                ('2024-11-25', 'Chi tiêu', 'Văn phòng phẩm', 'Giấy in', 30000.00, 'Chi phí văn phòng phẩm', '{username}'),
                ('2024-12-01', 'Thu nhập', 'Lương', 'Lương tháng 12', 5700000.00, 'Lương tháng 12', '{username}'),
                ('2024-12-08', 'Chi tiêu', 'Thể thao', 'Thuê sân bóng', 500000.00, 'Chi phí thuê sân', '{username}'),
                ('2024-12-12', 'Chi tiêu', 'Từ thiện', 'Quyên góp nhà thờ', 300000.00, 'Hoạt động từ thiện', '{username}'),
                ('2024-12-18', 'Chi tiêu', 'Tiêu dùng khác', 'Chi phí công cộng', 200000.00, 'Chi phí không dự kiến', '{username}'),
                ('2024-12-25', 'Thu nhập', 'Tiền từ hợp tác', 'Doanh thu từ hợp tác tháng 12', 1200000.00, 'Doanh thu hợp tác', '{username}'),
                ('2025-01-03', 'Chi tiêu', 'Cá nhân', 'Mua sách', 90000.00, 'Mua sách mới', '{username}'),
                ('2025-01-07', 'Thu nhập', 'Lương', 'Lương tháng 1', 5800000.00, 'Lương tháng 1', '{username}'),
                ('2025-01-15', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 280000.00, 'Chi phí ăn uống', '{username}'),
                ('2025-01-20', 'Chi tiêu', 'Sức khỏe', 'Thuốc', 90000.00, 'Chi phí thuốc men', '{username}'),
                ('2025-01-25', 'Thu nhập', 'Kinh doanh', 'Doanh thu tháng 1', 2200000.00, 'Doanh thu từ kinh doanh', '{username}'),
                ('2025-01-30', 'Chi tiêu', 'Đầu tư', 'Mua cổ phiếu', 320000.00, 'Đầu tư cổ phiếu', '{username}'),
                ('2025-02-05', 'Chi tiêu', 'Học tập', 'Khóa học trực tuyến', 130000.00, 'Chi phí học tập', '{username}'),
                ('2025-02-10', 'Thu nhập', 'Lãi suất ngân hàng', 'Lãi suất tháng 2', 160000.00, 'Lãi suất từ ngân hàng', '{username}'),
                ('2025-02-15', 'Chi tiêu', 'Giải trí', 'Đi xem phim', 110000.00, 'Chi phí giải trí', '{username}'),
                ('2025-02-20', 'Chi tiêu', 'Ăn uống', 'Nhà hàng', 210000.00, 'Chi phí ăn nhà hàng', '{username}'),
                ('2025-02-25', 'Chi tiêu', 'Nhà cửa', 'Tiền thuê nhà', 2600000.00, 'Tiền thuê nhà tháng 2', '{username}'),
                ('2025-03-01', 'Thu nhập', 'Lương', 'Lương tháng 3', 5900000.00, 'Lương tháng 3', '{username}'),
                ('2025-03-08', 'Chi tiêu', 'Du lịch', 'Chuyến đi Phú Quốc', 3100000.00, 'Chi phí du lịch', '{username}'),
                ('2025-03-15', 'Chi tiêu', 'Mua sắm', 'Quần áo', 160000.00, 'Mua quần áo mới', '{username}'),
                ('2025-03-20', 'Chi tiêu', 'Y tế', 'Khám bệnh', 130000.00, 'Khám sức khỏe định kỳ', '{username}'),
                ('2025-03-25', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 3', 600000.00, 'Thu nhập từ cổ tức', '{username}')""")
        conn.commit()
        conn.close()
        # Inform the user of success
        print("Sample transaction added successfully.")
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def verify_user_email(username, email):
    try:
        # Use 'with' to automatically manage the connection and ensure it closes
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            # Check if a user exists with the provided username and email
            cursor.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
            user = cursor.fetchone()
            return user is not None  # Returns True if user exists, False otherwise
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def verify_user_info(username, email, security_answer):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND email=? AND security_answer=?", (username, email, security_answer))
    user = cursor.fetchone()
    connection.close()
    return user is not None

def get_security_question(username):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT security_question FROM users WHERE username=?", (username,))
    user = cursor.fetchone()  # This returns a tuple like (security_question,)
    connection.close()
    if user:  # Check if user is not None
        return user[0]  # Return the first element of the tuple (the security question)
    else:
        return None

def update_user_password(username, new_password):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    connection.commit()
    updated_rows = cursor.rowcount
    connection.close()

    return updated_rows > 0
#login_account
def login(username, password):
    """Check if the user exists with the provided username and password."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

#add_transactions
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
            messagebox.showinfo("Success", "Transaction added successfully!")  # Success message
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")  # Error message

def get_text_color(value):
    """Return color based on the value."""
    return "red" if value < 0 else "green"

#get_summary
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

#get_transactions
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

#search_transactions
import sqlite3

def search_transactions(transaction_name=None, transaction_type="All", group_name="All", date_range="All", username=""):
    """Search transactions based on filters: transaction name, transaction type, group name, and date range.

    Args:
        transaction_name (str): Name of the transaction to search for.
        transaction_type (str): Type of the transaction (e.g., 'Income', 'Expense', or 'All').
        group_name (str): Name of the group to filter by (or 'All' for no filtering).
        date_range (str): Time range for transactions ('Today', 'Last 7 Days', 'Last 30 Days', or 'All').
        username (str): Username to filter transactions by.

    Returns:
        list: A list of tuples representing the transactions that match the search criteria.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Base query
    query = """
        SELECT id, transaction_date, transaction_type, group_name, transaction_name, amount, note
        FROM transactions
        WHERE username = ?
    """
    params = [username]

    # Filter by transaction name if provided
    if transaction_name and transaction_name != "All":
        query += " AND transaction_name LIKE ?"
        params.append(f"%{transaction_name}%")

    # Dynamic date filtering
    date_filters = {
        "Today": "DATE(transaction_date) = DATE('now')",
        "Last 7 Days": "DATE(transaction_date) >= DATE('now', '-7 days')",
        "Last 30 Days": "DATE(transaction_date) >= DATE('now', '-30 days')"
    }
    
    if date_range != "All":
        if date_range in date_filters:
            query += f" AND {date_filters[date_range]}"

    # Filter by transaction type if not 'All'
    if transaction_type != "All":
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    # Filter by group name if not 'All'
    if group_name != "All":
        query += " AND group_name = ?"
        params.append(group_name)

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        results = []
    finally:
        conn.close()

    return results


def delete_from_database(transaction_id):
    """Remove the transaction from the database based on the transaction ID."""
    try:
        # Establish a connection to the database
        connection = sqlite3.connect(DATABASE)  # Replace with your database file or connection details
        cursor = connection.cursor()
        
        # Execute the DELETE command
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        
        # Commit the changes
        connection.commit()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        print(f"Transaction with ID {transaction_id} has been deleted from the database.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
#get_unique_values
def get_unique_values(column_name):
    """Fetch unique values for a given column from the transactions table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = f"SELECT DISTINCT {column_name} FROM transactions"
    cursor.execute(query)
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results
#get_personal_info
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

#et_options_from_db
def get_options_from_db(query):
    """Get options from the database for dropdowns."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    options = [row[0] for row in cursor.fetchall()]
    conn.close()
    return options

# get_data
def get_data(query):
    """Retrieve data based on the provided SQL query."""
    conn = sqlite3.connect(DATABASE)  # Replace DATABASE with your actual database path
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
