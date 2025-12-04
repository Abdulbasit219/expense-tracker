import customtkinter as ctk
from tkinter import messagebox
from db import insert_db, update_db
from datetime import datetime

def render(root, refresh_callback, expenses, expense_index=None, accent="#1abc9c"):
    # Clear root
    for w in root.winfo_children():
        w.destroy()

    is_edit = expense_index is not None
    edit_id = None
    pre_desc = ""
    pre_amt = ""
    pre_cat = "Food"

    if is_edit:
        row = expenses[expense_index]
        edit_id = row[0]
        pre_desc = row[1]
        pre_amt = str(row[2])
        pre_cat = row[3]

    wrapper = ctk.CTkFrame(root)
    wrapper.pack(fill="both", expand=True, padx=20, pady=20)

    header = ctk.CTkLabel(wrapper, text="Edit Expense" if is_edit else "Add Expense", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(anchor="nw", pady=(6,12))

    form = ctk.CTkFrame(wrapper)
    form.pack(fill="x", pady=(8,12))

    ctk.CTkLabel(form, text="Description").grid(row=0, column=0, sticky="w", padx=6, pady=6)
    desc_entry = ctk.CTkEntry(form, width=520)
    desc_entry.grid(row=1, column=0, sticky="w", padx=6)
    desc_entry.insert(0, pre_desc)

    ctk.CTkLabel(form, text="Amount (PKR)").grid(row=2, column=0, sticky="w", padx=6, pady=(12,6))
    amt_entry = ctk.CTkEntry(form, width=240)
    amt_entry.grid(row=3, column=0, sticky="w", padx=6)
    amt_entry.insert(0, pre_amt)

    ctk.CTkLabel(form, text="Category").grid(row=2, column=1, sticky="w", padx=6, pady=(12,6))
    categories = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
    cat_menu = ctk.CTkOptionMenu(form, values=categories)
    cat_menu.grid(row=3, column=1, sticky="w", padx=6)
    cat_menu.set(pre_cat if pre_cat in categories else categories[0])


    ctk.CTkLabel(form, text="Date (YYYY-MM-DD) - optional").grid(row=4, column=0, sticky="w", padx=6, pady=(12,4))
    date_entry = ctk.CTkEntry(form, width=240)
    date_entry.grid(row=5, column=0, sticky="w", padx=6)
    date_entry.insert(0, "")


    btn_frame = ctk.CTkFrame(wrapper, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(18,6))

    def save_action():
        desc = desc_entry.get().strip()
        amt = amt_entry.get().strip()
        cat = cat_menu.get()

        if not desc or not amt:
            messagebox.showwarning("Missing", "Please enter both description and amount.")
            return
        try:
            amt_v = float(amt)
        except ValueError:
            messagebox.showerror("Invalid", "Amount must be numeric.")
            return

        dt_text = date_entry.get().strip()
        dt_iso = None
        if dt_text:
            try:
                
                dt_parsed = datetime.strptime(dt_text, "%Y-%m-%d")
                dt_iso = dt_parsed.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                messagebox.showerror("Invalid date", "Date must be YYYY-MM-DD")
                return

        if is_edit:
            update_db(desc, amt_v, cat, edit_id)
            messagebox.showinfo("Updated", "Expense updated.")
        else:
            insert_db(desc, amt_v, cat, dt_iso)
            messagebox.showinfo("Saved", "Expense added.")

        refresh_callback()

    save_btn = ctk.CTkButton(btn_frame, text="Save", fg_color=accent, width=120, command=save_action)
    save_btn.pack(side="left", padx=(8,12))

    cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", fg_color="transparent", border_color=accent, command=refresh_callback)
    cancel_btn.pack(side="left")