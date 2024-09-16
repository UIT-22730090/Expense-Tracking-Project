from ui import *
from expense_backend import *

if __name__ == "__main__":
    create_tables()  
    root = tk.Tk()
    app = LoginWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()