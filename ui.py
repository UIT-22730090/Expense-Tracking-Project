import tkinter as tk
from tkinter import messagebox, ttk, TclError, PhotoImage, Button, Label
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Expense Manager Login")
        master.geometry("400x300")

        tk.Label(master, text="Powered by nhóm 2", font=("Garamond", 8)).pack(anchor='nw')
        tk.Label(master, text="Welcome to Expense App", font=("Garamond", 16)).pack(pady=20)

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.forgot_button = tk.Button(master, text="Forgot Password?", fg="blue", relief=tk.FLAT, command=self.forgot_password)
        self.forgot_button.pack(side=tk.LEFT, padx=(20, 0))

        self.register_button = tk.Button(master, text="Register", fg="blue", relief=tk.FLAT, command=self.register)
        self.register_button.pack(side=tk.RIGHT, padx=(0, 20))

        master.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def login(self):
        pass

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Please contact support to reset your password.")

    def register(self):
        messagebox.showinfo("Register", "Register functionality coming soon.")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.quit()  # Use quit() to exit the mainloop and close the window

class MainApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("Expense Manager")
        master.geometry("800x600")

        self.menu_frame = tk.Frame(master, width=240)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.info_frame = tk.Frame(master, width=560)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # Define the path to the images directory
        self.images_path = os.path.join(os.path.dirname(__file__), 'images')
        
        self.setup_menu()
        self.show_summary()

    def setup_menu(self):
        self.user_image = Image.open(r'Image/user.png')
        self.user_image = self.user_image.resize((100, 100), Image.LANCZOS)
        self.user_image_tk = ImageTk.PhotoImage(self.user_image)
        
        user_image_label = tk.Label(self.menu_frame, image=self.user_image_tk)
        user_image_label.pack(pady=10)
        
        user_label = tk.Label(self.menu_frame, text=f"User: {self.username}", font=("Garamond", 14))
        user_label.pack(pady=5)

        buttons = [
            ("Tổng quát", self.show_summary, r'Image/user.png'),
            ("Thêm giao dịch", self.add_transaction, r'Image/overview.png'),
            ("Thống kê", self.show_statistics, r'Image/Add_Transaction.png'),
            ("Tìm kiếm giao dịch", self.search_transaction, r'Image/analytics.png'),
            ("Thông tin cá nhân", self.show_personal_info, r'Image/personal_information.png')
        ]

        for btn_text, btn_command, icon_path in buttons:
            button_frame = tk.Frame(self.menu_frame)
            button_frame.pack(fill=tk.X, pady=5)
            
            icon = Image.open(icon_path)
            icon = icon.resize((20, 20), Image.LANCZOS)
            icon_tk = ImageTk.PhotoImage(icon)
            
            button = tk.Button(
                button_frame, text=btn_text, image=icon_tk, compound=tk.LEFT, command=btn_command,
                width=150,padx=10, pady=5)
            button.pack(fill=tk.X, expand=True)
            button.image = icon_tk

    def show_summary(self):
        pass

    def add_transaction(self):
        pass

    def save_transaction(self, date, transaction_type, group_name, transaction_name, amount, note):
        pass

    def show_statistics(self):
        pass

    def display_bar_chart(self, ax, data, title, palette='viridis'):
        pass

    def search_transaction(self):
        pass

    def perform_search(self, transaction_name, transaction_type, group_name, date_range):
        pass

    def show_personal_info(self):
        pass
        
    def confirm_logout(self):
        """Prompt the user to confirm log out"""
        response = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if response:
            self.logout()

    def logout(self):
        """Handle user logout and navigate to the login window"""
        self.master.destroy()  # Close the current window
        login_window = tk.Tk()
        app = LoginWindow(login_window)
        login_window.mainloop()
