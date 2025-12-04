import customtkinter as ctk
from tkinter import messagebox
from db import delete_db
from add_expense import render as render_add

def render(root, back_callback, go_edit_callback, expenses, accent="#1abc9c"):
    for w in root.winfo_children():
        w.destroy()

    header = ctk.CTkFrame(root, fg_color="transparent")
    header.pack(fill="x", padx=16, pady=(12,10))
    ctk.CTkLabel(header, text="All Expenses", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
    ctk.CTkButton(header, text="Back", fg_color="transparent", border_color=accent, command=back_callback).pack(side="right")

    body = ctk.CTkScrollableFrame(root)
    body.pack(fill="both", expand=True, padx=16, pady=(6,16))

    if not expenses:
        ctk.CTkLabel(body, text="No expenses recorded yet.", text_color="#95a5a6").pack(pady=24)
        return


    sorted_exp = sorted(expenses, key=lambda x: x[4], reverse=True)
    header_row = ctk.CTkFrame(body, fg_color="#222222")
    header_row.pack(fill="x", padx=6, pady=(6,4))
    ctk.CTkLabel(header_row, text="Date", width=18).pack(side="left", padx=6)
    ctk.CTkLabel(header_row, text="Description", width=32).pack(side="left", padx=6)
    ctk.CTkLabel(header_row, text="Category", width=18).pack(side="left", padx=6)
    ctk.CTkLabel(header_row, text="Amount (PKR)", width=18).pack(side="left", padx=6)
    ctk.CTkLabel(header_row, text="Actions", width=20).pack(side="left", padx=6)

    for idx, r in enumerate(sorted_exp):
        fid, desc, amt, cat, dt = r
        row = ctk.CTkFrame(body, fg_color="#242424", corner_radius=6)
        row.pack(fill="x", padx=6, pady=6)

        ctk.CTkLabel(row, text=dt[:10], width=18).pack(side="left", padx=6)
        ctk.CTkLabel(row, text=desc, width=32, anchor="w").pack(side="left", padx=6)
        ctk.CTkLabel(row, text=cat, width=18).pack(side="left", padx=6)
        ctk.CTkLabel(row, text=f"PKR {amt:,.2f}", width=18, anchor="e", text_color="#ff6b6b").pack(side="left", padx=6)


        try:
            original_index = next(i for i, e in enumerate(expenses) if e[0] == fid)
        except StopIteration:
            original_index = None

        action_frame = ctk.CTkFrame(row, fg_color="transparent")
        action_frame.pack(side="left", padx=6)

        def on_delete(eid=fid):
            if messagebox.askyesno("Confirm", "Delete this expense?"):
                delete_db(eid)
                messagebox.showinfo("Deleted", "Expense removed.")
                back_callback()

        del_btn = ctk.CTkButton(action_frame, text="Delete", fg_color="#e74c3c", command=on_delete, width=80)
        del_btn.pack(side="left", padx=(0,6))

        def on_edit(orig_i=original_index):
            if orig_i is not None:
                # navigate to add/edit with index
                go_edit_callback(orig_i)

        edit_btn = ctk.CTkButton(action_frame, text="Edit", fg_color="#f39c12", width=80, command=on_edit)
        edit_btn.pack(side="left")