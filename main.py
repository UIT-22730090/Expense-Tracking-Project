from ui import *
from expense_backend import *
from install_dependencies import install_packages

if __name__ == "__main__":
    # Install necessary Python packages (this assumes Python is already installed)
    install_packages()  # Function that uses subprocess to install required packages
    # Create tables in the database
    create_tables()  
    # Start the UI
    root = tk.Tk()
    app = LoginWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
