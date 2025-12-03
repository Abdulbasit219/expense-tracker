import tkinter as tk

def create_add_expense_form(root, go_home, expenses, expense_index=None):
    """
    Add/Edit Expense Form based on expense_index
    """
    # Clear previous widgets in content_frame only
    for widget in root.winfo_children():
        widget.destroy()

    is_edit_mode = expense_index is not None

    # Title and button text 
    title_text = "📝 Edit Expense" if is_edit_mode else "➕ Add New Expense"
    button_text = "💾 Update Expense" if is_edit_mode else "➕ Add Expense"

    pre_desc = ""
    pre_amount = ""
    pre_cat = "Food"

    if is_edit_mode:
        exp_item = expenses[expense_index]
        pre_desc = exp_item[0]
        pre_amount = str(exp_item[1])
        pre_cat_backend = exp_item[2]

    main_frame = tk.Frame(root, bg="#D7E9F7")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add Expense Heading
    tk.Label(
        main_frame,
        text=title_text,
        font=("Arial", 28, "bold"),
        bg="#D7E9F7",
        fg="#2C3E50"
    ).pack(pady=(0, 30))

    form_frame = tk.Frame(main_frame, bg="#D7E9F7")
    form_frame.pack()

    # Styling function 
    def style_label(parent, text):
        return tk.Label(parent, text=text, font=("Arial", 14, "bold"), bg="#D7E9F7", fg="#555555")

    def style_entry(parent):
        return tk.Entry(parent, font=("Arial", 16), width=35, fg="#333333", 
                        relief="solid", highlightthickness=1, highlightbackground="#AAAAAA")

    # Description
    style_label(form_frame, "Description").pack(anchor="w", padx=10)
    desc_entry = style_entry(form_frame)
    desc_entry.insert(0, pre_desc)
    desc_entry.pack(pady=(5, 20), padx=10, ipady=8) 

    # Amount
    style_label(form_frame, "Amount (PKR)").pack(anchor="w", padx=10)
    amount_entry = style_entry(form_frame)
    amount_entry.insert(0, pre_amount)
    amount_entry.pack(pady=(5, 20), padx=10, ipady=8)

    # Category
    style_label(form_frame, "Category").pack(anchor="w", padx=10)
    category_options = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
    category_var = tk.StringVar()
    # category_var.set(category_options[0])   

    # Edit mode
    if is_edit_mode:
        for opt in category_options:
            if opt.startswith(pre_cat_backend):
                category_var.set(opt)
                break
    else:
        category_var.set(category_options[0])

    category_dropdown = tk.OptionMenu(form_frame, category_var, *category_options)
    category_dropdown.config(font=("Arial", 14), width=31, bg="#FFFFFF", fg="#2C3E50", 
                             activebackground="#F0F0F0", relief="solid", highlightthickness=1)                
    category_dropdown["menu"].config(font=("Arial", 12))
    category_dropdown.pack(pady=(5, 30), padx=10, ipady=5)

    button_frame = tk.Frame(main_frame, bg="#D7E9F7")
    button_frame.pack(pady=10)

    # Add Expense Button
    add_button = tk.Button(
        button_frame,
        text=button_text,  
        font=("Arial", 14, "bold"),
        bg="#28a745", # Greencolor
        fg="#FFFFFF",
        width=18,                
        height=2,
        relief="flat",
        cursor="hand2",
        activebackground="#218838",                
        activeforeground="#FFFFFF"
    )
    add_button.pack(side="left", padx=10)

    # Back Button
    back_button = tk.Button(
        button_frame, 
        text="🔙 Back to Home", 
        font=("Arial", 14, "bold"),
        bg="#DC3545", 
        fg="#FFFFFF",                
        width=18,                
        height=2,
        relief="flat",                
        cursor="hand2",
        command=go_home,                
        activebackground="#C82333",                
        activeforeground="#FFFFFF"
    )
    back_button.pack(side="left", padx=10)
