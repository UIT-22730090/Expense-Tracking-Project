import tkinter as tk
from tkinter import messagebox, ttk, TclError, PhotoImage, Button, Label
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
from expense_backend import *
import os


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
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = login(username, password)
        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.master.destroy()
            main_window = tk.Tk()
            app = MainApp(main_window, username)
            main_window.protocol("WM_DELETE_WINDOW", self.on_close)  # Set close protocol
            main_window.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def forgot_password(self):
        forgot_window = tk.Toplevel(self.master)
        forgot_window.title("Forgot Password")
        forgot_window.geometry("400x200")

        # First window to enter username and email
        tk.Label(forgot_window, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        username_entry = tk.Entry(forgot_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(forgot_window, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        email_entry = tk.Entry(forgot_window)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        def verify_username_email():
            username = username_entry.get().strip()
            email = email_entry.get().strip()

            # Check if username and email are valid
            if verify_user_email(username, email):  # Assuming verify_user_email() checks user info in DB
                # Close the first window and open the next window for security question
                forgot_window.destroy()

                # Create a new window for security question and password reset
                reset_password_window = tk.Toplevel(self.master)
                reset_password_window.title("Security Question")
                reset_password_window.geometry("400x300")

                security_question = get_security_question(username)

                tk.Label(reset_password_window, text=f"{security_question}: ").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                security_answer_entry = tk.Entry(reset_password_window)
                security_answer_entry.grid(row=0, column=1, padx=10, pady=5)

                def verify_security_and_reset():
                    security_answer = security_answer_entry.get().strip()

                    # Verify security answer
                    if verify_user_info(username, email, security_answer):
                        # Open another window to enter new password
                        new_password_window = tk.Toplevel(reset_password_window)
                        new_password_window.title("Reset Password")
                        new_password_window.geometry("400x200")

                        tk.Label(new_password_window, text="New Password:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
                        new_password_entry = tk.Entry(new_password_window, show="*")
                        new_password_entry.grid(row=0, column=1, padx=10, pady=5)

                        tk.Label(new_password_window, text="Re-enter New Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
                        re_new_password_entry = tk.Entry(new_password_window, show="*")
                        re_new_password_entry.grid(row=1, column=1, padx=10, pady=5)

                        def update_password():
                            new_password = new_password_entry.get().strip()
                            re_new_password = re_new_password_entry.get().strip()

                            if new_password == re_new_password:
                                # Update the password in the database
                                if update_user_password(username, new_password):
                                    messagebox.showinfo("Password Reset", "Your password has been successfully reset.")
                                    new_password_window.destroy()
                                    reset_password_window.destroy()
                                else:
                                    messagebox.showerror("Error", "Unable to reset password.")
                            else:
                                messagebox.showerror("Error", "Passwords do not match.")

                        submit_new_password_button = tk.Button(new_password_window, text="Submit", command=update_password)
                        submit_new_password_button.grid(row=2, column=0, columnspan=2, pady=10)
                    else:
                        messagebox.showerror("Verification Failed", "Invalid security answer. Please try again.")

                submit_security_button = tk.Button(reset_password_window, text="Submit", command=verify_security_and_reset)
                submit_security_button.grid(row=1, column=0, columnspan=2, pady=10)

            else:
                messagebox.showerror("Error", "Invalid username or email.")

        submit_button = tk.Button(forgot_window, text="Submit", command=verify_username_email)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)


    def register(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("400x550")

        # Create input fields
        tk.Label(register_window, text="Full Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        full_name_entry = tk.Entry(register_window)
        full_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        username_entry = tk.Entry(register_window)
        username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        password_entry = tk.Entry(register_window, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Re-enter Password:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        re_password_entry = tk.Entry(register_window, show="*")
        re_password_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Birthday (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        birthday_entry = DateEntry(register_window, date_pattern="yyyy-mm-dd")
        birthday_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Email:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        email_entry = tk.Entry(register_window)
        email_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(register_window, text="Phone Number:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        phone_entry = tk.Entry(register_window)
        phone_entry.grid(row=6, column=1, padx=10, pady=5)

        # Security question dropdown
        tk.Label(register_window, text="Select a Security Question:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        security_question_var = tk.StringVar(register_window)
        security_question_options = ["What is your pet's name?", "What is your mother's maiden name?", 
                                    "What was the name of your first school?", "What is your favorite book?"]
        security_question_menu = tk.OptionMenu(register_window, security_question_var, *security_question_options)
        security_question_menu.grid(row=7, column=1, padx=10, pady=5)

        # Security answer entry
        tk.Label(register_window, text="Answer:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        security_answer_entry = tk.Entry(register_window)
        security_answer_entry.grid(row=8, column=1, padx=10, pady=5)

        # Variable to store the selected option for sample transaction
        sample_var = tk.StringVar(value="Yes")

        tk.Label(register_window, text="Create Sample Transaction:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
        tk.Radiobutton(register_window, text="Yes", variable=sample_var, value="Yes").grid(row=9, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(register_window, text="No", variable=sample_var, value="No").grid(row=9, column=1, padx=10, pady=5, sticky="e")

        def submit_action():
            # Retrieve the input from the fields
            full_name = full_name_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            re_password = re_password_entry.get().strip()
            birthday = birthday_entry.get().strip()
            email = email_entry.get().strip()
            phone_number = phone_entry.get().strip()
            security_question = security_question_var.get()
            security_answer = security_answer_entry.get().strip()
            sample = sample_var.get()

            # Validate and register the user
            if register_user(full_name, username, password, re_password, birthday, email, phone_number, security_question, security_answer):
                if sample == "Yes":
                    add_sample_transaction(username)
                register_window.destroy()

        submit_button = tk.Button(register_window, text="Submit", command=submit_action)
        submit_button.grid(row=10, column=0, columnspan=2, pady=10)
        
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
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Retrieve all transactions and convert to DataFrame
        transactions = get_transactions(self.username)
        df = pd.DataFrame(transactions, columns=['Date', 'Type', 'Group', 'Name', 'Amount', 'Note'])

        # Convert 'Date' to datetime and 'Amount' to numeric
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

        # Extract month-year from the date
        df['MonthYear'] = df['Date'].dt.to_period('M')

        # Calculate totals and balance
        total_income = df[df['Type'] == 'Thu nhập']['Amount'].sum()
        total_expense = df[df['Type'] == 'Chi tiêu']['Amount'].sum()
        balance = total_income - total_expense

        # Create a frame for the totals box
        totals_frame = tk.Frame(self.info_frame, borderwidth=0, relief='groove')
        totals_frame.pack(pady=10, padx=10, fill=tk.X)

        # Configure grid in totals_frame
        totals_frame.grid_rowconfigure(0, weight=1)
        totals_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Add labels to the same row in the totals_frame
        tk.Label(
            totals_frame,
            text=f"Total Income: {total_income:,.0f}",
            font=("Garamond", 15, "bold"),
            fg="black"
        ).grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        tk.Label(
            totals_frame,
            text=f"Total Expense: {total_expense:,.0f}",
            font=("Garamond", 15, "bold"),
            fg="black"
        ).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(
            totals_frame,
            text=f"Balance: {balance:,.0f}",
            font=("Garamond", 15, "bold"),
            fg=get_text_color(balance)
        ).grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        # Group by month-year and type, then calculate total income and expenses
        monthly_summary = df.groupby(['MonthYear', 'Type'])['Amount'].sum().unstack().fillna(0).reset_index()
        monthly_summary.rename(columns={'Thu nhập': 'Total Income', 'Chi tiêu': 'Total Expense'}, inplace=True)
        
        # Calculate total income, expense, and balance by month-year
        monthly_summary['Balance'] = monthly_summary['Total Income'] - monthly_summary['Total Expense']

        # Plotting
        fig, axs = plt.subplots(2, 1, figsize=(5, 5))

        # Plot Total Income and Expenses
        axs[0].plot(monthly_summary['MonthYear'].astype(str), monthly_summary['Total Income'], label='Total Income', color='green', marker='o')
        axs[0].plot(monthly_summary['MonthYear'].astype(str), monthly_summary['Total Expense'], label='Total Expense', color='red', marker='o')
        axs[0].set_title('Total Income and Expenses by Month')
        axs[0].set_xlabel('Month-Year')
        axs[0].set_ylabel('Amount')
        axs[0].legend()

        # Plot Balance by Month
        axs[1].plot(monthly_summary['MonthYear'].astype(str), monthly_summary['Balance'], color='blue', marker='o')
        axs[1].set_title('Balance by Month')
        axs[1].set_xlabel('Month-Year')
        axs[1].set_ylabel('Balance')

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.info_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_transaction(self):
        # Clear the current frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the inputs
        input_frame = tk.Frame(self.info_frame)
        input_frame.pack(pady=10)

        # Arrange inputs in 3 rows
        # First row: Date, Transaction Type, Group Name
        tk.Label(input_frame, text="Date:", font=("Garamond", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = DateEntry(input_frame)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Transaction Type:", font=("Garamond", 12)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        transaction_type = ttk.Combobox(
            input_frame, 
            values=get_options_from_db("SELECT DISTINCT type_name FROM transaction_types")
        )
        transaction_type.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Group Name:", font=("Garamond", 12)).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        group_name = ttk.Combobox(
            input_frame, 
            values=get_options_from_db("SELECT DISTINCT group_name FROM transaction_types")
        )
        group_name.grid(row=0, column=5, padx=5, pady=5)

        # Second row: Transaction Name, Amount, Note
        tk.Label(input_frame, text="Transaction Name:", font=("Garamond", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        transaction_name = tk.Entry(input_frame)
        transaction_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Amount:", font=("Garamond", 12)).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        amount = tk.Entry(input_frame)
        amount.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Note:", font=("Garamond", 12)).grid(row=1, column=4, padx=5, pady=5, sticky="e")
        note = tk.Entry(input_frame)
        note.grid(row=1, column=5, padx=5, pady=5)

        # Save transaction button
        save_button = tk.Button(
            self.info_frame, 
            text="Save Transaction", 
            command=lambda: self.save_transaction(
                date_entry.get(), transaction_type.get(), group_name.get(), 
                transaction_name.get(), amount.get(), note.get()
            )
        )
        save_button.pack(pady=10)

        # Create a frame for the Treeview and scrollbars
        tree_frame = tk.Frame(self.info_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Creating a Treeview (table) to display transactions
        columns = ('Date', 'Type', 'Group', 'Name', 'Amount', 'Note')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')

        # Create vertical scrollbar
        v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scroll.pack(side="right", fill="y")

        # Create horizontal scrollbar
        h_scroll = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        h_scroll.pack(side="bottom", fill="x")

        # Configure Treeview to use the scrollbars
        tree.configure(yscrollcommand=v_scroll.set)
        tree.configure(xscrollcommand=h_scroll.set)

        # Fetch and insert transactions into the table
        transactions = get_transactions(self.username)
        for transaction in transactions:
            tree.insert('', 'end', values=transaction)

    def save_transaction(self, date, transaction_type, group_name, transaction_name, amount, note):
        """Handle the save transaction button click."""
        # Add the transaction to the database
        add_transactions(date, transaction_type, group_name, transaction_name, float(amount), note, self.username)
        messagebox.showinfo("Success", "Transaction added successfully!")
        # Refresh the transaction table
        self.add_transaction()

    def show_statistics(self):
        # Clear the current frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Frame for displaying the charts
        chart_frame = tk.Frame(self.info_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        transaction_types = ['Thu nhập', 'Chi tiêu']
        queries = {
            'by_note': "SELECT note, SUM(amount) FROM transactions WHERE transaction_type = '{}' AND username = '{}' GROUP BY note ORDER BY SUM(amount) DESC",
            'by_group': "SELECT group_name, SUM(amount) FROM transactions WHERE transaction_type = '{}' AND username = '{}' GROUP BY group_name ORDER BY SUM(amount) DESC",
            'by_name': "SELECT transaction_name, SUM(amount) FROM transactions WHERE transaction_type = '{}' AND username = '{}' GROUP BY transaction_name ORDER BY SUM(amount) DESC"
        }

        data = {}
        for t in transaction_types:
            for key, query in queries.items():
                try:
                    result = get_data(query.format(t, self.username))
                    data[f"{t}_{key}"] = result if result else [(None, 0)]  # Handle no data case
                except Exception as e:
                    print(f"Error fetching data for {t} - {key}: {e}")
                    data[f"{t}_{key}"] = [(None, 0)]  # Handle error case

        # Create a figure with subplots
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.10, wspace=0.2, hspace=1)

        chart_titles = {
            'Thu nhập_by_group': "Total Income by Group",
            'Thu nhập_by_name': "Total Income by Name",
            'Thu nhập_by_note': "Detail Total Income",
            'Chi tiêu_by_group': "Expense by Group",
            'Chi tiêu_by_name': "Expense by Name",
            'Chi tiêu_by_note': "Detail Total Expense"
        }

        for idx, (key, title) in enumerate(chart_titles.items()):
            row, col = divmod(idx, 3)
            self.display_bar_chart(axs[row, col], data[key], title)

        # Convert the figure to a Tkinter canvas and display it
        canvas = FigureCanvasTkAgg(fig, master=self.info_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def display_bar_chart(self, ax, data, title, palette='viridis'):
        """Display a bar chart in the given axes."""
        df = pd.DataFrame(data, columns=['Label', 'Amount'])
        sns.barplot(x='Label', y='Amount', data=df, ax=ax, palette=palette)
        ax.set_title(title)
        ax.set_xlabel('')
        ax.set_ylabel('Amount')

        # Setting ticks explicitly
        ax.set_xticks(range(len(df['Label'])))
        ax.set_xticklabels(df['Label'], rotation=45, ha='right')

    def search_transaction(self):
        # Clear the current frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Add a title or instruction label
        tk.Label(self.info_frame, text="Search Transactions", font=("Garamond", 12)).grid(row=0, columnspan=9, pady=10)

        # Transaction Name Entry
        tk.Label(self.info_frame, text="Transaction Name:", font=("Garamond", 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        transaction_name_combobox = ttk.Combobox(self.info_frame, values=get_unique_values("transaction_name") + ["All"], state="readonly")
        transaction_name_combobox.current(len(get_unique_values("transaction_name")))  # Default to "All"
        transaction_name_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Transaction Type Combobox
        tk.Label(self.info_frame, text="Transaction Type:", font=("Garamond", 10)).grid(row=1, column=2, padx=5, pady=5, sticky='e')
        transaction_type_combobox = ttk.Combobox(self.info_frame, values=get_unique_values("transaction_type") + ["All"], state="readonly")
        transaction_type_combobox.current(len(get_unique_values("transaction_type")))  # Default to "All"
        transaction_type_combobox.grid(row=1, column=3, padx=5, pady=5)

        # Group Name Combobox
        tk.Label(self.info_frame, text="Group Name:", font=("Garamond", 10)).grid(row=1, column=4, padx=5, pady=5, sticky='e')
        group_name_combobox = ttk.Combobox(self.info_frame, values=get_unique_values("group_name") + ["All"], state="readonly")
        group_name_combobox.current(len(get_unique_values("group_name")))  # Default to "All"
        group_name_combobox.grid(row=1, column=5, padx=5, pady=5)

        # Date Range Combobox
        tk.Label(self.info_frame, text="Date Range:", font=("Garamond", 10)).grid(row=1, column=6, padx=5, pady=5, sticky='e')
        date_range_combobox = ttk.Combobox(self.info_frame, values=["Today", "Last 7 Days", "Last 30 Days", "All Time"], state="readonly")
        date_range_combobox.current(3)  # Default to "All Time"
        date_range_combobox.grid(row=1, column=7, padx=5, pady=5)

        # Search Button
        search_button = tk.Button(self.info_frame, text="Search", command=lambda: self.perform_search(
            transaction_name_combobox.get(),
            transaction_type_combobox.get(),
            group_name_combobox.get(),
            date_range_combobox.get()
        ))
        search_button.grid(row=2, columnspan=9, pady=10)

        # Create a frame for the Treeview and scrollbars
        tree_frame = tk.Frame(self.info_frame)
        tree_frame.grid(row=3, columnspan=9, padx=5, pady=10, sticky='nsew')

        # Create Treeview widget
        self.results_table = ttk.Treeview(tree_frame, columns=("ID", "Date", "Type", "Group", "Name", "Amount", "Note", "Actions"), show='headings')
        self.results_table.heading("ID", text="ID")
        self.results_table.heading("Date", text="Date")
        self.results_table.heading("Type", text="Type")
        self.results_table.heading("Group", text="Group")
        self.results_table.heading("Name", text="Name")
        self.results_table.heading("Amount", text="Amount")
        self.results_table.heading("Note", text="Note")
        self.results_table.heading("Actions", text="Actions")  # New heading for the button

        # Create vertical scrollbar
        v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=self.results_table.yview)
        v_scroll.pack(side="right", fill="y")

        # Create horizontal scrollbar
        h_scroll = tk.Scrollbar(tree_frame, orient="horizontal", command=self.results_table.xview)
        h_scroll.pack(side="bottom", fill="x")

        # Configure Treeview to use the scrollbars
        self.results_table.configure(yscrollcommand=v_scroll.set)
        self.results_table.configure(xscrollcommand=h_scroll.set)

        # Pack Treeview widget
        self.results_table.pack(fill=tk.BOTH, expand=True)

        # Configure row and column weights for resizing
        for col in range(9):
            self.info_frame.grid_columnconfigure(col, weight=1)
        self.info_frame.grid_rowconfigure(3, weight=1)

    def perform_search(self, transaction_name, transaction_type, group_name, date_range):
        """Collects filter values, performs the search, and displays results."""
        # Fetch search results using the filters
        search_results = search_transactions(transaction_name, transaction_type, group_name, date_range, username = self.username)

        # Clear previous search results in the table
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        # Insert new results into the table with a "Delete" link
        for result in search_results:
            transaction_id, date, type_, group, name, amount, note = result
            # Add a delete link text to the "Actions" column
            self.results_table.insert("", "end", values=(transaction_id, date, type_, group, name, amount, note, "Delete"), tags=("action",))

        # Bind click event to the "Delete" link text
        self.results_table.bind("<ButtonRelease-1>", self.handle_action_click)
        
    def handle_action_click(self, event):
        """Handle click events on the 'Actions' column."""
        item = self.results_table.identify_row(event.y)
        if not item:
            return

        col = self.results_table.identify_column(event.x)
        if col == "#8":  # Check if the click was in the 'Actions' column
            transaction_id = self.results_table.item(item, "values")[0]
            self.confirm_delete(transaction_id)

    def confirm_delete(self, transaction_id):
        """Ask for confirmation before deleting a row."""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            self.delete_row(transaction_id)
        
    def delete_row(self, transaction_id):
        """Delete a row from the Treeview and database based on the transaction ID."""
        # Remove from Treeview
        for item in self.results_table.get_children():
            if self.results_table.item(item, "values")[0] == transaction_id:
                self.results_table.delete(item)
                break
        # Remove from database using the external module function
        delete_from_database(transaction_id)

    def show_personal_info(self):
        """Display personal information in a popup window."""
        # Create a new Toplevel window using the correct main window reference
        popup = tk.Toplevel(self.master)  # Use self.master or the correct reference to the main window
        popup.title("Thông tin cá nhân")  # Title of the popup window

        # Load the image (replace 'path_to_image.png' with your actual image path)
        try:
            # For PNG, GIF, and other Tkinter-supported formats:
            img = PhotoImage(file=r'Image/user.png')
            # If using PIL for JPG, etc.:
            # pil_image = Image.open('path_to_image.jpg')
            # img = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            img = None  # Handle the case where the image can't be loaded

        # Create and place the button with image
        if img:  # Check if the image loaded successfully
            info_button = Button(popup, text="Thông tin cá nhân", image=img, compound='top', command=lambda: None)
            info_button.image = img  # Keep a reference to avoid garbage collection
            info_button.pack(pady=10)  # Adjust padding as needed

        # Display personal information content in the popup window
        try:
            info = get_personal_info(self.username)  # Fetch personal information
            Label(popup, text=f"Tên: {info['full_name']}", font=("Garamond", 14)).pack(anchor='w', padx=10, pady=5)
            Label(popup, text=f"Ngày sinh: {info['birthday']}", font=("Garamond", 14)).pack(anchor='w', padx=10, pady=5)
            Label(popup, text=f"Email: {info['email']}", font=("Garamond", 14)).pack(anchor='w', padx=10, pady=5)
            Label(popup, text=f"Số điện thoại: {info['phone_number']}", font=("Garamond", 14)).pack(anchor='w', padx=10, pady=5)
        except Exception as e:
            print(f"Error fetching personal information: {e}")

        # Add Log Out Button
        logout_button = Button(popup, text="Log Out", command=self.confirm_logout)
        logout_button.pack(pady=10)
    
    def show_personal_info_V1(self):
        #for widget in self.info_frame.winfo_children():
            #widget.destroy()

        # Simulated personal info fetching
        #info = get_personal_info(self.username)

        # Display user image and personal information
        #image_path = info.get('image_path')
        #if image_path:
            #try:
                #img = Image.open(image_path)
                #img = img.resize((100, 100), Image.LANCZOS)
                #img_tk = ImageTk.PhotoImage(img)
                #img_label = tk.Label(self.info_frame, image=img_tk)
                #img_label.image = img_tk
                #img_label.pack(pady=10)
            #except Exception as e:
                #print(f"Error loading image: {e}")
                #tk.Label(self.info_frame, text="Error loading image.", font=("Garamond", 12)).pack(pady=10)

        #for key, value in info.items():
            #if key != 'image_path':
                #tk.Label(self.info_frame, text=f"{key.capitalize()}: {value}", font=("Garamond", 12)).pack(pady=5)

        # Add Log Out Button
        #logout_button = tk.Button(self.info_frame, text="Log Out", command=self.confirm_logout)
        #logout_button.pack(pady=10)
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
     
if __name__ == "__main__":
    create_tables()  
    root = tk.Tk()
    app = LoginWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
