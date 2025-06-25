# budget_logic.py
from typing import List
from models import Expense, Budget, ExpenseManager

def calculate_total_spent(expenses: List[Expense], category: str) -> float:
    return sum(e.amount for e in expenses if e.category == category)

def check_budget(manager: ExpenseManager, category: str) -> float:
    total = calculate_total_spent(manager.get_expenses(), category)
    budget = manager.get_budget(category)
    return total - budget.limit if budget else 0.0

def check_all_budgets(manager: ExpenseManager):
    budgets = manager.get_all_budgets()
    overspending = {}
    for budget in budgets:
        diff = check_budget(manager, budget.category)
        if diff > 0:
            overspending[budget.category] = diff
    return overspending