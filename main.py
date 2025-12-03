import tkinter as tk
from add_expense import create_add_expense_form
from home import show_home
from view_expenses import show_all_expenses

expenses = [
    ["Hafta bhar ka samaan", 6500.00, "Food", "2025-11-28"],
    ["Bike ka petrol", 1800.00, "Transport", "2025-11-27"],
    ["Nayi film ki tickets", 1500.00, "Entertainment", "2025-11-26"],
    ["Online shoes kharide", 9000.00, "Shopping", "2025-11-25"],
    ["Bijli ka bill", 4800.00, "Utility", "2025-11-24"],
    ["Lunch with colleagues", 950.00, "Food", "2025-11-23"],
    ["Bus/Taxi fare", 700.00, "Transport", "2025-11-22"],
    ["Gym membership fee", 3000.00, "Other", "2025-11-20"],
    ["Birthday gift", 2500.00, "Shopping", "2025-11-19"],
    ["Dinner party", 3500.00, "Food", "2025-11-18"],
]

root = tk.Tk()
root.title("Expense Tracker")
root.attributes("-fullscreen", True)
root.config(bg="#D7E9F7")
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# ---------- Top Frame for Title ----------
top_frame = tk.Frame(root, bg="#D7E9F7")
top_frame.pack(fill="x")

title = tk.Label(
    top_frame,
    text="Expense Tracker",
    font=("Times New Roman", 34, "bold"),
    bg="#D7E9F7",
    fg="#2C3E50"
)
title.pack(pady=20)

# Content Frame 
content_frame = tk.Frame(root, bg="#D7E9F7")
content_frame.pack(fill="both", expand=True)

# Navigation Functions
def go_home():
    show_home(content_frame, go_to_add_expense, expenses, go_to_view_expenses)

def go_to_add_expense():
    create_add_expense_form(content_frame, go_home, expenses)  

def go_to_view_expenses():
    show_all_expenses(content_frame, go_home, expenses)

# Start Home 
go_home()

root.mainloop()
