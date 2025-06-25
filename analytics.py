# analytics.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import ExpenseManager

def generate_report(currency="$"):
    manager = ExpenseManager()
    df = pd.DataFrame([e.__dict__ for e in manager.get_expenses()])
    if df.empty:
        return None
    df['amount'] = df['amount'].astype(float)
    summary = df.groupby('category')['amount'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    summary.plot(kind='pie', y='amount', labels=summary['category'], autopct='%1.1f%%', ax=ax)
    plt.title(f"Spending by Category ({currency})")
    return fig

def show_chart_in_window(parent_window, currency="$"):
    fig = generate_report(currency)
    if fig:
        canvas = FigureCanvasTkAgg(fig, master=parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack()