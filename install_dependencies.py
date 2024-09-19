import subprocess
import sys

def install_packages():
    # List of third-party packages (exclude standard libraries like tkinter and sqlite3)
    required_packages = ["Pillow", "tkcalendar", "matplotlib", "seaborn", "pandas", "sqlite3"]
    
    # Install all packages at once
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_packages)
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install some packages: {str(e)}")
