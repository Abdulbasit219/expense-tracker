import tkinter as tk
from tkinter import ttk
from add_expense import create_add_expense_form

def show_all_expenses(root, back_to_home_func, expenses):
    # Clear previous widgets in the content frame                
    for widget in root.winfo_children():                
        widget.destroy()

    # Heading Frame                
    header_frame = tk.Frame(root, bg="#D7E9F7")                
    header_frame.pack(fill="x", pady=(30, 20), padx=60)                

    tk.Label(                
        header_frame,                
        text="All Expenses List",                
        font=("Times New Roman", 28, "bold"),                
        bg="#D7E9F7",                
        fg="#2C3E50"                
    ).pack(side="left")

    # Back to Home Button                
    back_button = tk.Button(                
        header_frame,                
        text="< Back to Home",                
        font=("Arial", 14, "bold"),                
        bg="#6C757D",                 
        fg="#FFFFFF",                
        padx=15,                
        pady=5,                
        command=back_to_home_func,                
        cursor="hand2",                
    )                
    back_button.pack(side="right")

    # Table Container
    table_container = tk.Frame(root, bg="#D7E9F7")                
    table_container.pack(fill="both", expand=True, padx=60, pady=10)                

    # Table Headers                
    headers = ["Date", "Description", "Category", "Amount (PKR)", "Actions"]                
    col_widths = [15, 35, 20, 18, 15]
    
    header_row_frame = tk.Frame(table_container, bg="#F1F1F1")                
    header_row_frame.pack(fill="x")                

    for col, header in enumerate(headers):                
        tk.Label(header_row_frame, text=header, font=("Arial", 12, "bold"), bg="#F1F1F1", fg="#2C3E50",                
                 padx=10, pady=10, width=col_widths[col], anchor="w" if col<3 else "c", relief="solid").pack(side="left", fill="x", expand=True)

    # Data Container                 
    data_container = tk.Frame(table_container, bg="#FFFFFF")                
    data_container.pack(fill="both", expand=True)                

    def delete_expense(index):                
        print(f"Delete expense at index: {index}")

    # Sort expenses                 
    sorted_expenses = sorted(expenses, key=lambda x: x[3], reverse=True)                

    # Row display                
    for row_num, exp in enumerate(sorted_expenses):                
        date, description, category, amount = exp[3], exp[0], exp[2], f"{exp[1]:,.2f}"                
        
        # Alternate row coloring for better readability                
        bg_color = "#FFFFFF" if row_num % 2 == 0 else "#F8F9FA"                
        
        row_frame = tk.Frame(data_container, bg=bg_color)                
        row_frame.pack(fill="x")                
        
        data_color = "#343A40"                
        
        tk.Label(row_frame, text=date, font=("Arial", 12), bg=bg_color, fg=data_color,                
                 padx=10, pady=8, width=col_widths[0], anchor="w").pack(side="left", fill="x", expand=True)                
        
        tk.Label(row_frame, text=description, font=("Arial", 12), bg=bg_color, fg=data_color,                
                 padx=10, pady=8, width=col_widths[1], anchor="w").pack(side="left", fill="x", expand=True)                
        
        tk.Label(row_frame, text=category, font=("Arial", 12), bg=bg_color, fg=data_color,                
                 padx=10, pady=8, width=col_widths[2], anchor="w").pack(side="left", fill="x", expand=True)                
        
        tk.Label(row_frame, text=amount, font=("Arial", 12, "bold"), bg=bg_color, fg="#DC3545",                
                 padx=10, pady=8, width=col_widths[3], anchor="e").pack(side="left", fill="x", expand=True)                
        
        # ACTION BUTTONS
        action_frame = tk.Frame(row_frame, bg=bg_color, width=col_widths[4])                
        action_frame.pack(side="left", fill="x", expand=True, padx=5)

        # Edit Button
        edit_btn = tk.Button(
            action_frame, 
            text="✎ Edit", 
            font=("Arial", 10), 
            bg="#ffc107", 
            fg="#000", 
            bd=1, 
            relief="solid", 
            cursor="hand2", 
            command=lambda i=row_num: create_add_expense_form(root, back_to_home_func, expenses, i))                
        edit_btn.pack(side="left", padx=2, pady=5)                
        
        # Delete Button
        del_btn = tk.Button(action_frame, text="🗑 Delete", font=("Arial", 10), bg="#dc3545", fg="#fff", bd=1, relief="solid", cursor="hand2", command=lambda r=row_num: delete_expense(r))                
        del_btn.pack(side="left", padx=2, pady=5)

    if not sorted_expenses:                
        tk.Label(data_container, text="No expenses recorded yet.", font=("Arial", 14, "italic"),                
                 bg="#FFFFFF", fg="#6C757D", pady=30).pack()