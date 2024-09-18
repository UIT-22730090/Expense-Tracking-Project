import sqlite3

    #Create database
def create_database():
    conn = sqlite3.connect('expense_manager.db')
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
    # Create transaction types table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL,  -- 'Thu nhập' or 'Chi tiêu'
            group_name TEXT NOT NULL  -- 'Gia đình', 'Cá nhân', etc.
        )
    ''')

    # Create transactions table
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

     # Insert sample data into users table
    cursor.execute("INSERT OR IGNORE INTO users (username, password, full_name, birthday, email, phone_number) VALUES ('user1', '123', 'Nguyễn Nhóm 2', '2024-09-11', 'Nhoms2@ms.uit.edu.vn', '090xxxxxxxx')")

    # Insert sample data into transaction_types table
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
    # Insert sample data into transactions table
    cursor.execute('''
                INSERT OR IGNORE INTO transactions (transaction_date, transaction_type, group_name, transaction_name, amount, note, username)
                VALUES
                ('2024-01-03', 'Chi tiêu', 'Cá nhân', 'Mua sách', 80000.00, 'Mua sách mới', 'user1'),
                ('2024-01-07', 'Thu nhập', 'Lương', 'Lương tháng 1', 5000000.00, 'Lương tháng 1', 'user1'),
                ('2024-01-15', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 250000.00, 'Chi phí ăn uống', 'user1'),
                ('2024-01-20', 'Chi tiêu', 'Sức khỏe', 'Thuốc', 75000.00, 'Chi phí thuốc men', 'user1'),
                ('2024-01-25', 'Thu nhập', 'Kinh doanh', 'Doanh thu tháng 1', 2000000.00, 'Doanh thu từ kinh doanh', 'user1'),
                ('2024-01-30', 'Chi tiêu', 'Đầu tư', 'Mua cổ phiếu', 300000.00, 'Đầu tư cổ phiếu', 'user1'),
                ('2024-02-05', 'Chi tiêu', 'Học tập', 'Khóa học trực tuyến', 120000.00, 'Chi phí học tập', 'user1'),
                ('2024-02-10', 'Thu nhập', 'Lãi suất ngân hàng', 'Lãi suất tháng 2', 150000.00, 'Lãi suất từ ngân hàng', 'user1'),
                ('2024-02-15', 'Chi tiêu', 'Giải trí', 'Đi xem phim', 100000.00, 'Chi phí giải trí', 'user1'),
                ('2024-02-20', 'Chi tiêu', 'Ăn uống', 'Nhà hàng', 200000.00, 'Chi phí ăn nhà hàng', 'user1'),
                ('2024-02-25', 'Chi tiêu', 'Nhà cửa', 'Tiền thuê nhà', 2500000.00, 'Tiền thuê nhà tháng 2', 'user1'),
                ('2024-03-01', 'Thu nhập', 'Lương', 'Lương tháng 3', 5100000.00, 'Lương tháng 3', 'user1'),
                ('2024-03-08', 'Chi tiêu', 'Du lịch', 'Chuyến đi Đà Lạt', 3000000.00, 'Chi phí du lịch', 'user1'),
                ('2024-03-15', 'Chi tiêu', 'Mua sắm', 'Quần áo', 150000.00, 'Mua quần áo mới', 'user1'),
                ('2024-03-20', 'Chi tiêu', 'Y tế', 'Khám bệnh', 120000.00, 'Khám sức khỏe định kỳ', 'user1'),
                ('2024-03-25', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 3', 500000.00, 'Thu nhập từ cổ tức', 'user1'),
                ('2024-04-02', 'Chi tiêu', 'Dịch vụ', 'Cắt tóc', 60000.00, 'Chi phí cắt tóc', 'user1'),
                ('2024-04-07', 'Thu nhập', 'Tiền thưởng', 'Thưởng quý 1', 1200000.00, 'Thưởng công việc', 'user1'),
                ('2024-04-10', 'Chi tiêu', 'Trợ cấp', 'Trợ cấp cho cha mẹ', 300000.00, 'Hỗ trợ cha mẹ', 'user1'),
                ('2024-04-15', 'Chi tiêu', 'Hóa đơn', 'Tiền điện', 400000.00, 'Hóa đơn tiền điện tháng 4', 'user1'),
                ('2024-04-20', 'Chi tiêu', 'Giao thông', 'Xăng xe', 180000.00, 'Chi phí xăng xe', 'user1'),
                ('2024-04-25', 'Thu nhập', 'Tiền bán tài sản', 'Bán xe máy cũ', 3500000.00, 'Bán xe cũ', 'user1'),
                ('2024-05-01', 'Thu nhập', 'Lương', 'Lương tháng 5', 5200000.00, 'Lương tháng 5', 'user1'),
                ('2024-05-05', 'Chi tiêu', 'Bảo hiểm', 'Bảo hiểm y tế', 500000.00, 'Chi phí bảo hiểm', 'user1'),
                ('2024-05-12', 'Chi tiêu', 'Thực phẩm', 'Mua thực phẩm', 220000.00, 'Chi phí thực phẩm', 'user1'),
                ('2024-05-18', 'Thu nhập', 'Quà tặng', 'Nhận quà sinh nhật', 200000.00, 'Quà sinh nhật', 'user1'),
                ('2024-05-23', 'Chi tiêu', 'Giáo dục', 'Đóng học phí', 1500000.00, 'Chi phí học phí', 'user1'),
                ('2024-05-28', 'Chi tiêu', 'Văn phòng phẩm', 'Mua bút viết', 30000.00, 'Chi phí văn phòng phẩm', 'user1'),
                ('2024-06-01', 'Thu nhập', 'Lương', 'Lương tháng 6', 5300000.00, 'Lương tháng 6', 'user1'),
                ('2024-06-08', 'Chi tiêu', 'Thể thao', 'Mua đồ tập gym', 400000.00, 'Chi phí thể thao', 'user1'),
                ('2024-06-12', 'Chi tiêu', 'Từ thiện', 'Quyên góp từ thiện', 200000.00, 'Hoạt động từ thiện', 'user1'),
                ('2024-06-18', 'Chi tiêu', 'Tiêu dùng khác', 'Chi phí linh tinh', 100000.00, 'Chi phí không dự kiến', 'user1'),
                ('2024-06-25', 'Thu nhập', 'Tiền từ hợp tác', 'Doanh thu từ hợp tác', 1000000.00, 'Doanh thu hợp tác', 'user1'),
                ('2024-07-02', 'Chi tiêu', 'Cá nhân', 'Mua điện thoại mới', 2000000.00, 'Chi phí mua điện thoại', 'user1'),
                ('2024-07-06', 'Thu nhập', 'Đầu tư', 'Thu nhập đầu tư', 600000.00, 'Thu nhập từ đầu tư', 'user1'),
                ('2024-07-12', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 250000.00, 'Chi phí ăn uống', 'user1'),
                ('2024-07-18', 'Chi tiêu', 'Sức khỏe', 'Bảo hiểm sức khỏe', 250000.00, 'Bảo hiểm sức khỏe', 'user1'),
                ('2024-07-22', 'Chi tiêu', 'Phương tiện', 'Sửa xe máy', 350000.00, 'Chi phí sửa xe', 'user1'),
                ('2024-07-28', 'Thu nhập', 'Thù lao', 'Thù lao dự án', 800000.00, 'Thù lao công việc', 'user1'),
                ('2024-08-01', 'Thu nhập', 'Lương', 'Lương tháng 8', 5400000.00, 'Lương tháng 8', 'user1'),
                ('2024-08-06', 'Chi tiêu', 'Học tập', 'Mua sách học tập', 70000.00, 'Chi phí mua sách', 'user1'),
                ('2024-08-10', 'Chi tiêu', 'Giải trí', 'Mua game', 300000.00, 'Chi phí giải trí', 'user1'),
                ('2024-08-15', 'Chi tiêu', 'Ăn uống', 'Nhà hàng Nhật', 500000.00, 'Chi phí nhà hàng', 'user1'),
                ('2024-08-20', 'Chi tiêu', 'Nhà cửa', 'Sửa nhà', 1000000.00, 'Chi phí sửa nhà', 'user1'),
                ('2024-08-25', 'Thu nhập', 'Doanh thu khác', 'Doanh thu tháng 8', 1500000.00, 'Doanh thu khác', 'user1'),
                ('2024-09-01', 'Thu nhập', 'Lương', 'Lương tháng 9', 5500000.00, 'Lương tháng 9', 'user1'),
                ('2024-09-05', 'Chi tiêu', 'Du lịch', 'Du lịch Nha Trang', 4000000.00, 'Chi phí du lịch', 'user1'),
                ('2024-09-12', 'Chi tiêu', 'Mua sắm', 'Mua đồ dùng gia đình', 200000.00, 'Chi phí mua sắm', 'user1'),
                ('2024-09-18', 'Chi tiêu', 'Y tế', 'Thuốc bổ', 80000.00, 'Chi phí thuốc bổ', 'user1'),
                ('2024-09-23', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 9', 700000.00, 'Thu nhập từ cổ tức', 'user1'),
                ('2024-10-02', 'Chi tiêu', 'Dịch vụ', 'Cắt cỏ sân vườn', 120000.00, 'Chi phí cắt cỏ', 'user1'),
                ('2024-10-07', 'Thu nhập', 'Tiền thưởng', 'Thưởng quý 3', 1300000.00, 'Thưởng công việc', 'user1'),
                ('2024-10-10', 'Chi tiêu', 'Trợ cấp', 'Trợ cấp cho người thân', 400000.00, 'Hỗ trợ người thân', 'user1'),
                ('2024-10-15', 'Chi tiêu', 'Hóa đơn', 'Tiền nước', 300000.00, 'Hóa đơn tiền nước', 'user1'),
                ('2024-10-20', 'Chi tiêu', 'Giao thông', 'Vé xe buýt', 50000.00, 'Chi phí giao thông', 'user1'),
                ('2024-10-25', 'Thu nhập', 'Tiền bán tài sản', 'Bán điện thoại cũ', 500000.00, 'Bán điện thoại cũ', 'user1'),
                ('2024-11-01', 'Thu nhập', 'Lương', 'Lương tháng 11', 5600000.00, 'Lương tháng 11', 'user1'),
                ('2024-11-05', 'Chi tiêu', 'Bảo hiểm', 'Bảo hiểm xe', 700000.00, 'Chi phí bảo hiểm xe', 'user1'),
                ('2024-11-10', 'Chi tiêu', 'Thực phẩm', 'Mua rau củ', 50000.00, 'Chi phí thực phẩm', 'user1'),
                ('2024-11-15', 'Thu nhập', 'Quà tặng', 'Quà sinh nhật từ bạn', 100000.00, 'Quà sinh nhật', 'user1'),
                ('2024-11-20', 'Chi tiêu', 'Giáo dục', 'Sách giáo khoa', 150000.00, 'Chi phí giáo dục', 'user1'),
                ('2024-11-25', 'Chi tiêu', 'Văn phòng phẩm', 'Giấy in', 30000.00, 'Chi phí văn phòng phẩm', 'user1'),
                ('2024-12-01', 'Thu nhập', 'Lương', 'Lương tháng 12', 5700000.00, 'Lương tháng 12', 'user1'),
                ('2024-12-08', 'Chi tiêu', 'Thể thao', 'Thuê sân bóng', 500000.00, 'Chi phí thuê sân', 'user1'),
                ('2024-12-12', 'Chi tiêu', 'Từ thiện', 'Quyên góp nhà thờ', 300000.00, 'Hoạt động từ thiện', 'user1'),
                ('2024-12-18', 'Chi tiêu', 'Tiêu dùng khác', 'Chi phí công cộng', 200000.00, 'Chi phí không dự kiến', 'user1'),
                ('2024-12-25', 'Thu nhập', 'Tiền từ hợp tác', 'Doanh thu từ hợp tác tháng 12', 1200000.00, 'Doanh thu hợp tác', 'user1'),
                ('2025-01-03', 'Chi tiêu', 'Cá nhân', 'Mua sách', 90000.00, 'Mua sách mới', 'user1'),
                ('2025-01-07', 'Thu nhập', 'Lương', 'Lương tháng 1', 5800000.00, 'Lương tháng 1', 'user1'),
                ('2025-01-15', 'Chi tiêu', 'Gia đình', 'Tiền ăn', 280000.00, 'Chi phí ăn uống', 'user1'),
                ('2025-01-20', 'Chi tiêu', 'Sức khỏe', 'Thuốc', 90000.00, 'Chi phí thuốc men', 'user1'),
                ('2025-01-25', 'Thu nhập', 'Kinh doanh', 'Doanh thu tháng 1', 2200000.00, 'Doanh thu từ kinh doanh', 'user1'),
                ('2025-01-30', 'Chi tiêu', 'Đầu tư', 'Mua cổ phiếu', 320000.00, 'Đầu tư cổ phiếu', 'user1'),
                ('2025-02-05', 'Chi tiêu', 'Học tập', 'Khóa học trực tuyến', 130000.00, 'Chi phí học tập', 'user1'),
                ('2025-02-10', 'Thu nhập', 'Lãi suất ngân hàng', 'Lãi suất tháng 2', 160000.00, 'Lãi suất từ ngân hàng', 'user1'),
                ('2025-02-15', 'Chi tiêu', 'Giải trí', 'Đi xem phim', 110000.00, 'Chi phí giải trí', 'user1'),
                ('2025-02-20', 'Chi tiêu', 'Ăn uống', 'Nhà hàng', 210000.00, 'Chi phí ăn nhà hàng', 'user1'),
                ('2025-02-25', 'Chi tiêu', 'Nhà cửa', 'Tiền thuê nhà', 2600000.00, 'Tiền thuê nhà tháng 2', 'user1'),
                ('2025-03-01', 'Thu nhập', 'Lương', 'Lương tháng 3', 5900000.00, 'Lương tháng 3', 'user1'),
                ('2025-03-08', 'Chi tiêu', 'Du lịch', 'Chuyến đi Phú Quốc', 3100000.00, 'Chi phí du lịch', 'user1'),
                ('2025-03-15', 'Chi tiêu', 'Mua sắm', 'Quần áo', 160000.00, 'Mua quần áo mới', 'user1'),
                ('2025-03-20', 'Chi tiêu', 'Y tế', 'Khám bệnh', 130000.00, 'Khám sức khỏe định kỳ', 'user1'),
                ('2025-03-25', 'Thu nhập', 'Cổ tức', 'Cổ tức tháng 3', 600000.00, 'Thu nhập từ cổ tức', 'user1')
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()