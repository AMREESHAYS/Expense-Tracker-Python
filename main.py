# main.py
import ttkbootstrap as ttk
from ui import ExpenseTrackerApp

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = ExpenseTrackerApp(root)
    root.mainloop()