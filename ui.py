# ui.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from models import ExpenseManager, Expense, Budget
from budget_logic import check_all_budgets
from notifier import send_scold
from analytics import show_chart_in_window
from ocr_module import extract_text_from_receipt
from tkinter import filedialog, messagebox, Listbox
import json
import os

class ExpenseTrackerApp:
    CONFIG_FILE = "config.json"
    DEFAULT_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker That Yells at You")
        self.root.geometry("800x600")
        self.manager = ExpenseManager()
        self.currency = "$"  # Default currency
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.load_config()

        self.notebook = ttk.Notebook(root, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.expense_tab = ttk.Frame(self.notebook, bootstyle="secondary")
        self.budget_tab = ttk.Frame(self.notebook, bootstyle="info")
        self.report_tab = ttk.Frame(self.notebook, bootstyle="success")
        self.settings_tab = ttk.Frame(self.notebook, bootstyle="warning")

        self.notebook.add(self.expense_tab, text="Expenses")
        self.notebook.add(self.budget_tab, text="Budgets")
        self.notebook.add(self.report_tab, text="Reports")
        self.notebook.add(self.settings_tab, text="Settings")

        self.build_expense_tab()
        self.build_budget_tab()
        self.build_report_tab()
        self.build_settings_tab()

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.currency = data.get("currency", self.currency)
                    self.categories = data.get("categories", self.categories)
            except Exception:
                pass

    def save_config(self):
        data = {
            "currency": self.currency,
            "categories": self.categories
        }
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def build_expense_tab(self):
        form_frame = ttk.LabelFrame(self.expense_tab, text="Add Expense", bootstyle="primary")
        form_frame.pack(pady=10, fill=X, padx=10)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=W, pady=2)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=0, column=1, pady=2)

        ttk.Label(form_frame, text="Amount:").grid(row=1, column=0, sticky=W, pady=2)
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=1, pady=2)

        ttk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=W, pady=2)
        self.category_var = ttk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=self.categories)
        self.category_combo.grid(row=2, column=1, pady=2)
        self.category_combo.set(self.categories[0])

        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=W, pady=2)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=3, column=1, pady=2)

        ttk.Button(form_frame, text="Add Expense", command=self.add_expense, bootstyle=SUCCESS).grid(row=4, columnspan=2, pady=5)

        self.expense_feedback = ttk.Label(self.expense_tab, text="", bootstyle="success")
        self.expense_feedback.pack()

        self.expense_tree = ttk.Treeview(self.expense_tab, columns=("ID", "Date", "Amount", "Category", "Description"), show="headings")
        self.expense_tree.heading("ID", text="ID")
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.heading("Amount", text=f"Amount ({self.currency})")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Description", text="Description")
        self.expense_tree.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.load_expenses()

    def load_expenses(self):
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)
        for exp in self.manager.get_expenses():
            self.expense_tree.insert("", END, values=(exp.id, exp.date, f"{self.currency}{exp.amount:.2f}", exp.category, exp.description))

    def add_expense(self):
        try:
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            desc = self.desc_entry.get()
            if category and category not in self.categories:
                self.categories.append(category)
                self.save_config()
                self.category_combo["values"] = self.categories
                self.budget_category_combo["values"] = self.categories
            exp = Expense(None, date, amount, category, desc)
            self.manager.add_expense(exp)
            self.load_expenses()
            self.check_budgets()
            self.expense_feedback.config(text="Expense added successfully!", bootstyle="success")
        except Exception as e:
            self.expense_feedback.config(text=f"Error: {e}", bootstyle="danger")

    def check_budgets(self):
        overspending = check_all_budgets(self.manager)
        for cat, amount in overspending.items():
            send_scold("severe" if amount > 100 else "moderate")

    def build_budget_tab(self):
        form_frame = ttk.LabelFrame(self.budget_tab, text="Set Budget", bootstyle="info")
        form_frame.pack(pady=10, fill=X, padx=10)

        ttk.Label(form_frame, text="Category:").grid(row=0, column=0, sticky=W, pady=2)
        self.budget_category_var = ttk.StringVar()
        self.budget_category_combo = ttk.Combobox(form_frame, textvariable=self.budget_category_var, values=self.categories)
        self.budget_category_combo.grid(row=0, column=1, pady=2)
        self.budget_category_combo.set(self.categories[0])

        ttk.Label(form_frame, text=f"Limit ({self.currency}):").grid(row=1, column=0, sticky=W, pady=2)
        self.budget_limit = ttk.Entry(form_frame)
        self.budget_limit.grid(row=1, column=1, pady=2)

        ttk.Button(form_frame, text="Set Budget", command=self.set_budget, bootstyle=INFO).grid(row=2, columnspan=2, pady=5)

        self.budget_feedback = ttk.Label(self.budget_tab, text="", bootstyle="success")
        self.budget_feedback.pack()

        self.budget_tree = ttk.Treeview(self.budget_tab, columns=("Category", "Limit"), show="headings")
        self.budget_tree.heading("Category", text="Category")
        self.budget_tree.heading("Limit", text=f"Limit ({self.currency})")
        self.budget_tree.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.load_budgets()

    def load_budgets(self):
        for row in self.budget_tree.get_children():
            self.budget_tree.delete(row)
        for budget in self.manager.get_all_budgets():
            self.budget_tree.insert("", END, values=(budget.category, f"{self.currency}{budget.limit:.2f}"))

    def set_budget(self):
        try:
            category = self.budget_category_var.get()
            limit = float(self.budget_limit.get())
            if not category:
                self.budget_feedback.config(text="Category cannot be empty!", bootstyle="danger")
                return
            if category and category not in self.categories:
                self.categories.append(category)
                self.save_config()
                self.category_combo["values"] = self.categories
                self.budget_category_combo["values"] = self.categories
            self.manager.set_budget(Budget(category, limit))
            self.load_budgets()
            self.budget_feedback.config(text="Budget set successfully!", bootstyle="success")
        except Exception as e:
            self.budget_feedback.config(text=f"Error: {e}", bootstyle="danger")

    def build_report_tab(self):
        ttk.Button(self.report_tab, text="Generate Report", command=lambda: show_chart_in_window(self.report_tab, self.currency), bootstyle=PRIMARY).pack(pady=10)
        # Chart will be injected here when button clicked

    def build_settings_tab(self):
        # Clear previous widgets if reloading
        for widget in self.settings_tab.winfo_children():
            widget.destroy()

        # --- General Settings Section ---
        general_frame = ttk.LabelFrame(self.settings_tab, text="General Settings", bootstyle="primary")
        general_frame.pack(fill=X, padx=10, pady=10)

        # Currency selection
        ttk.Label(general_frame, text="Currency:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=W, pady=5, padx=5)
        self.currency_var = ttk.StringVar(value=self.currency)
        currency_options = ["$", "€", "£", "₹", "¥"]
        self.currency_combo = ttk.Combobox(general_frame, textvariable=self.currency_var, values=currency_options, state="readonly")
        self.currency_combo.grid(row=0, column=1, pady=5, padx=5)
        self.currency_combo.bind("<<ComboboxSelected>>", self.change_currency)

        # Theme selection
        ttk.Label(general_frame, text="Theme:", font=("Helvetica", 11)).grid(row=1, column=0, sticky=W, pady=5, padx=5)
        self.theme_var = ttk.StringVar(value="auto")
        theme_options = ["auto", "light", "dark"]
        self.theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, values=theme_options, state="readonly")
        self.theme_combo.grid(row=1, column=1, pady=5, padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # --- Category Management Section ---
        cat_frame = ttk.LabelFrame(self.settings_tab, text="Manage Categories", bootstyle="info")
        cat_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(cat_frame, text="Add Category:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.new_cat_var = ttk.StringVar()
        self.new_cat_entry = ttk.Entry(cat_frame, textvariable=self.new_cat_var)
        self.new_cat_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(cat_frame, text="Add", command=self.add_category, bootstyle=SUCCESS).grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(cat_frame, text="Current Categories:").grid(row=1, column=0, sticky=NW, padx=5, pady=2)
        self.cat_listbox = Listbox(cat_frame, listvariable=ttk.StringVar(value=self.categories), height=6, selectmode="single")
        self.cat_listbox.grid(row=1, column=1, padx=5, pady=2, sticky=W)
        ttk.Button(cat_frame, text="Remove Selected", command=self.remove_category, bootstyle=DANGER).grid(row=1, column=2, padx=5, pady=2)

        # --- OCR Section ---
        ocr_frame = ttk.LabelFrame(self.settings_tab, text="Scan Receipt (OCR)", bootstyle="warning")
        ocr_frame.pack(fill=X, padx=10, pady=10)
        ttk.Button(ocr_frame, text="Scan Receipt", command=self.scan_receipt, bootstyle=SECONDARY).pack(pady=5)

    def add_category(self):
        new_cat = self.new_cat_var.get().strip()
        if new_cat and new_cat not in self.categories:
            self.categories.append(new_cat)
            self.save_config()
            self.category_combo["values"] = self.categories
            self.budget_category_combo["values"] = self.categories
            self.cat_listbox.delete(0, 'end')
            for cat in self.categories:
                self.cat_listbox.insert('end', cat)
            self.new_cat_var.set("")

    def remove_category(self):
        selected = self.cat_listbox.curselection()
        if selected:
            cat = self.cat_listbox.get(selected[0])
            if cat in self.categories:
                self.categories.remove(cat)
                self.save_config()
                self.category_combo["values"] = self.categories
                self.budget_category_combo["values"] = self.categories
                self.cat_listbox.delete(selected[0])

    def change_theme(self, event=None):
        # This is a placeholder for theme change logic. ttkbootstrap supports themes.
        # You can apply theme using: self.root.style.theme_use(self.theme_var.get())
        # For now, just print or store the theme.
        print(f"Theme changed to: {self.theme_var.get()}")

    def change_currency(self, event=None):
        self.currency = self.currency_var.get()
        self.save_config()
        # Update all UI elements with new currency
        self.expense_tree.heading("Amount", text=f"Amount ({self.currency})")
        self.budget_tree.heading("Limit", text=f"Limit ({self.currency})")
        self.load_expenses()
        self.load_budgets()

    def scan_receipt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            text = extract_text_from_receipt(file_path)
            print(f"[OCR] Extracted Text:\n{text}")
            messagebox.showinfo("OCR Result", text)