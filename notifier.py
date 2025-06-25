# notifier.py
import random
from tkinter import messagebox
from plyer import notification

SCOLD_MESSAGES = {
    "mild": [
        "You're getting close to your budget. Time to slow down!",
        "Almost there... maybe skip that coffee?",
    ],
    "moderate": [
        "Uh oh, you're over budget for this category.",
        "Your wallet just cried out in pain.",
    ],
    "severe": [
        "🚨 ALARM! Your spending is out of control!",
        "You've officially entered panic mode.",
    ]
}

def send_scold(severity: str = "mild"):
    msg = random.choice(SCOLD_MESSAGES.get(severity, ["Unknown issue"]))
    print(f"[SCOLD] {msg}")
    notification.notify(title="Budget Alert!", message=msg, timeout=5)
    messagebox.showwarning("Budget Alert", msg)
