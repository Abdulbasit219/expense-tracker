import customtkinter as ctk
from db import connect_db, load_all_expenses
import home as home_page
import add_expense as add_page
import view_expenses as view_page

ctk.set_appearance_mode("Dark")

ACCENT = "#1abc9c"  # teal

# --- App setup ---
connect_db()
root = ctk.CTk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.title("Expense Tracker — Dark Modern")
root.geometry("1200x760")
root.minsize(1000, 650)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- Sidebar ---
sidebar = ctk.CTkFrame(root, width=220, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="nswe")
sidebar.grid_rowconfigure(6, weight=1)

title_lbl = ctk.CTkLabel(sidebar, text="Expense Tracker", font=ctk.CTkFont(size=18, weight="bold"))
title_lbl.grid(row=0, column=0, padx=16, pady=(20, 10), sticky="w")


logo = ctk.CTkButton(sidebar, text="🏦", width=36, height=36, fg_color="transparent", hover=False)
logo.grid(row=1, column=0, padx=16, pady=(0, 20), sticky="w")


content_frame = ctk.CTkFrame(root, corner_radius=0)
content_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=18)


expenses = []

def reload_expenses():
    global expenses
    expenses = load_all_expenses()
    return expenses


def show_dashboard():
    reload_expenses()
    home_page.render(content_frame, go_add, go_view, expenses, ACCENT)

def go_add(expense_index=None):

    add_page.render(content_frame, show_dashboard, expenses, expense_index, ACCENT)

def go_view():
    reload_expenses()
    view_page.render(content_frame, show_dashboard, go_add, expenses, ACCENT)


btn_dashboard = ctk.CTkButton(sidebar, text="Dashboard", fg_color=ACCENT, hover_color="#16a085", command=show_dashboard)
btn_dashboard.grid(row=2, column=0, padx=16, pady=8, sticky="we")

btn_add = ctk.CTkButton(sidebar, text="Add Expense", fg_color="transparent", border_color=ACCENT, command=go_add)
btn_add.grid(row=3, column=0, padx=16, pady=8, sticky="we")

btn_view = ctk.CTkButton(sidebar, text="View Expenses", fg_color="transparent", border_color=ACCENT, command=go_view)
btn_view.grid(row=4, column=0, padx=16, pady=8, sticky="we")


footer = ctk.CTkLabel(sidebar, text="v1.0  •  Dark Teal", text_color="#95a5a6", font=ctk.CTkFont(size=11))
footer.grid(row=7, column=0, padx=16, pady=10, sticky="s")


show_dashboard()
root.mainloop()