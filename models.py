# models.py
import sqlite3
from typing import List, Optional
from datetime import datetime

class Expense:
    def __init__(self, eid: int, date: str, amount: float, category: str, description: str):
        self.id = eid
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

class Budget:
    def __init__(self, category: str, limit: float):
        self.category = category
        self.limit = limit

class ExpenseManager:
    def __init__(self, db_path: str = 'expenses.db'):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()

    def _initialize_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    category TEXT PRIMARY KEY,
                    "limit" REAL
                )
            """)

    def add_expense(self, expense: Expense):
        with self.conn:
            self.conn.execute(
                "INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                (expense.date, expense.amount, expense.category, expense.description)
            )

    def get_expenses(self) -> List[Expense]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return [Expense(*row) for row in cursor.fetchall()]

    def update_expense(self, expense: Expense):
        with self.conn:
            self.conn.execute(
                "UPDATE expenses SET date=?, amount=?, category=?, description=? WHERE id=?",
                (expense.date, expense.amount, expense.category, expense.description, expense.id)
            )

    def delete_expense(self, eid: int):
        with self.conn:
            self.conn.execute("DELETE FROM expenses WHERE id=?", (eid,))

    def set_budget(self, budget: Budget):
        with self.conn:
            self.conn.execute(
                'REPLACE INTO budgets (category, "limit") VALUES (?, ?)',  # Quoting "limit" to avoid SQL syntax error
                (budget.category, budget.limit)
            )

    def get_budget(self, category: str) -> Optional[Budget]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM budgets WHERE category=?", (category,))
        row = cursor.fetchone()
        return Budget(*row) if row else None

    def get_all_budgets(self) -> List[Budget]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM budgets")
        return [Budget(*row) for row in cursor.fetchall()]