import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

def calculate_summary(expenses):
    """Total expense aur category wise breakdown calculate karta hai."""
    total_expense = sum(item[1] for item in expenses)
    category_totals = {}
    for _, amount, category, _ in expenses:
        category_totals[category] = category_totals.get(category, 0.0) + amount
    return total_expense, category_totals

def plot_bar_chart(frame, category_totals):
    """Matplotlib chart banakar tkinter frame mein embed karta hai."""    

    # Figure             
    fig, ax = plt.subplots(figsize=(5, 3), dpi=80)                
    fig.patch.set_facecolor('#FFFFFF')  
    
    if category_totals:                
        categories = list(category_totals.keys())                
        amounts = list(category_totals.values())                
                        
        bars = ax.bar(categories, amounts, color='#007BFF')                
                        
        ax.set_title('Category Wise Spending', fontsize=12, fontweight='bold')                
        ax.set_ylabel('Amount (PKR)', fontsize=10)                
        plt.xticks(rotation=15, fontsize=8) 
        plt.yticks(fontsize=8)                
                        
    else:                
        ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center')                
        ax.set_title('Category Wise Spending', fontsize=12, fontweight='bold')                

    # Convert chart into tkinter                
    canvas = FigureCanvasTkAgg(fig, master=frame)                
    canvas.draw()                
    canvas.get_tk_widget().pack(fill="both", expand=True)

def calculate_time_based_summary(expenses):
    weekly_expense = 0
    monthly_expense = 0

    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    one_month_ago = now - timedelta(days=30)

    for _, amount, _, date_str in expenses:
        try:
            expense_date = datetime.strptime(date_str, "%Y-%m-%d")
            if expense_date >= one_week_ago:
                weekly_expense += amount
            if expense_date >= one_month_ago:
                monthly_expense += amount
        except ValueError:
            continue
    
    return weekly_expense, monthly_expense

def show_home(root, go_to_add_expense, expenses, go_to_view_expenses):
    """
    Complete Home Page showing summary and recent transactions.
    """
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Calculate summary data
    total_expense, category_totals = calculate_summary(expenses)

    weekly_expense, monthly_expense = calculate_time_based_summary(expenses)
    
    # Home Heading and Add Button Frame 
    header_frame = tk.Frame(root, bg="#D7E9F7")
    header_frame.pack(fill="x", pady=(30, 20), padx=60)

    tk.Label(
        header_frame,
        text="Dashboard Overview",
        font=("Times New Roman", 28, "bold"),
        bg="#D7E9F7",
        fg="#2C3E50"
    ).pack(side="left")

    # Buttons Container 
    buttons_frame = tk.Frame(header_frame, bg="#D7E9F7")
    buttons_frame.pack(side="right")

    # Export Button
    def export_action():
        print("Exporting to Excel...")

    export_button = tk.Button( 
        buttons_frame,
        text="📊 Export as Excel", 
        font=("Arial", 12, "bold"),                
        bg="#1D6F42", 
        fg="#FFFFFF",                
        padx=15,                
        pady=5,                
        command=export_action,                
        cursor="hand2",                
    )
    export_button.pack(side="left", padx=10)

    # View All Expenses
    view_button = tk.Button( 
        buttons_frame,
        text="👁 View All Expenses",   
        font=("Arial", 14, "bold"),
        bg="#007BFF", 
        fg="#FFFFFF",
        padx=15,
        pady=5,
        command=go_to_view_expenses, 
        cursor="hand2",
    )
    view_button.pack(side="left", padx=10)

    add_button = tk.Button( 
        buttons_frame,
        text=" + Add New Expense",   
        font=("Arial", 16, "bold"),
        bg="#28a745",                 
        fg="#FFFFFF",
        padx=15,
        pady=5,
        command=go_to_add_expense,
        cursor="hand2",
    )
    add_button.pack(side="right")

    # Main Content Area 
    content_area = tk.Frame(root, bg="#D7E9F7")
    content_area.pack(fill="both", expand=True, padx=60, pady=10)

    # Summary Card 
    summary_frame = tk.Frame(content_area, bg="#FFFFFF", padx=30, pady=20, 
                             highlightbackground="#2C3E50", highlightthickness=1)
    summary_frame.pack(fill="x", pady=20)
    
    tk.Label(summary_frame, text="Expense Summary", 
             font=("Arial", 18, "bold"), bg="#FFFFFF", fg="#2C3E50").pack(anchor="w")
    
    # Container frame jo left aur right dono ko hold karega
    inner_summary_container = tk.Frame(summary_frame, bg="#FFFFFF")
    inner_summary_container.pack(fill="x", pady=(15, 0))
    
    # LEFT Side Frame: Total Expenses (Bada aur Red)
    left_total_frame = tk.Frame(inner_summary_container, bg="#FFFFFF")
    left_total_frame.pack(side="left", anchor="nw")
    
    tk.Label(left_total_frame, text="Total", 
             font=("Arial", 14, "bold"), bg="#FFFFFF", fg="#555555").pack(anchor="w")
    
    # Bada Amount Label (Red color)
    tk.Label(left_total_frame, text=f"PKR {total_expense:,.2f}", 
             font=("Arial", 36, "bold"), bg="#FFFFFF", fg="#DC3545").pack(anchor="w")

    # RIGHT Side Frame: Weekly/Monthly (Chota font)
    right_details_frame = tk.Frame(inner_summary_container, bg="#FFFFFF", padx=20)
    right_details_frame.pack(side="right", anchor="ne", expand=True)
    
    # Styling for right details
    label_font = ("Arial", 11)
    amount_font = ("Arial", 12, "bold")
    detail_fg = "#343A40"
    
    
    # Weekly Detail
    tk.Label(right_details_frame, text="Weekly Total", 
             font=label_font, bg="#FFFFFF", fg="#555555").grid(row=0, column=0, sticky="w", padx=10)
    tk.Label(right_details_frame, text=f"PKR {weekly_expense:,.2f}", 
             font=amount_font, bg="#FFFFFF", fg=detail_fg).grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))
    
    # Monthly Detail
    tk.Label(right_details_frame, text="Monthly Total", 
             font=label_font, bg="#FFFFFF", fg="#555555").grid(row=0, column=1, sticky="w", padx=10)
    tk.Label(right_details_frame, text=f"PKR {monthly_expense:,.2f}", 
             font=amount_font, bg="#FFFFFF", fg=detail_fg).grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))
    

    breakdown_label = tk.Label(content_area, text="Spending Breakdown", 
                                font=("Arial", 20, "bold"), bg="#D7E9F7", fg="#2C3E50")
    breakdown_label.pack(anchor="w", pady=(30, 10))                

    # Container frame                 
    visualization_frame = tk.Frame(content_area, bg="#D7E9F7")                
    visualization_frame.pack(fill="x", pady=10)                

    #category text Breakdown                
    breakdown_text_frame = tk.Frame(visualization_frame, bg="#FFFFFF", padx=20, pady=10, 
                                highlightbackground="#2C3E50", highlightthickness=1)
    breakdown_text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    row_num = 0
    if category_totals:
        for category, total in category_totals.items():
            if total_expense:
                percentage = (total / total_expense) * 100  
            else:
                percentage = 0
            
            tk.Label(breakdown_text_frame, text=f"{category}:", 
                     font=("Arial", 12), bg="#FFFFFF", fg="#2C3E50", width=15, anchor="w").grid(row=row_num, column=0, sticky="w", pady=2)
            
            tk.Label(breakdown_text_frame, text=f"PKR {total:,.0f}", 
                     font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#007BFF", width=12, anchor="e").grid(row=row_num, column=1, sticky="e", pady=2, padx=5)
            
            tk.Label(breakdown_text_frame, text=f"({percentage:.1f}%)", 
                     font=("Arial", 11), bg="#FFFFFF", fg="#6C757D", width=8, anchor="e").grid(row=row_num, column=2, sticky="e", pady=2)
            
            row_num += 1
    else:
        tk.Label(breakdown_text_frame, text="No expenses recorded yet.", 
                 font=("Arial", 12, "italic"), bg="#FFFFFF", fg="#6C757D", padx=10, pady=10).pack()                

    #  Bar Chart                
    chart_frame = tk.Frame(visualization_frame, bg="#FFFFFF", highlightbackground="#2C3E50", highlightthickness=1)                
    chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))                
    
    # Chart function call                
    plot_bar_chart(chart_frame, category_totals)                

    # Recent Transactions List 
    recent_label = tk.Label(content_area, text="Recent Transactions", 
                             font=("Arial", 20, "bold"), bg="#D7E9F7", fg="#2C3E50")
    recent_label.pack(anchor="w", pady=(30, 10))

    recent_frame = tk.Frame(content_area, bg="#FFFFFF", highlightbackground="#2C3E50", highlightthickness=1)
    recent_frame.pack(fill="x")

    # Table Headers
    headers = ["Date", "Description", "Category", "Amount (PKR)"]
    col_widths = [15, 30, 30, 30]

    for col, header in enumerate(headers):
        tk.Label(recent_frame, text=header, font=("Arial", 14, "bold"), bg="#F1F1F1", fg="#2C3E50", 
                 padx=10, pady=8, width=col_widths[col], relief="solid").grid(row=0, column=col, sticky="nsew")

    # Display transactions 
    recent_expenses = sorted(expenses, key=lambda x: x[3], reverse=True)[:5] 
    
    for row_num, exp in enumerate(recent_expenses, start=1):
        date, description, category, amount = exp[3], exp[0], exp[2], f"{exp[1]:,.2f}"
        
        data_color = "#343A40"
        
        tk.Label(recent_frame, text=date, font=("Arial", 12), bg="#FFFFFF", fg=data_color, 
                 padx=10, pady=6, width=col_widths[0], anchor="w").grid(row=row_num, column=0, sticky="nsew")
        
        tk.Label(recent_frame, text=description, font=("Arial", 12), bg="#FFFFFF", fg=data_color, 
                 padx=10, pady=6, width=col_widths[1], anchor="w").grid(row=row_num, column=1, sticky="nsew")
        
        tk.Label(recent_frame, text=category, font=("Arial", 12), bg="#FFFFFF", fg=data_color, 
                 padx=10, pady=6, width=col_widths[2], anchor="w").grid(row=row_num, column=2, sticky="nsew")
        
        tk.Label(recent_frame, text=amount, font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#DC3545", 
                 padx=10, pady=6, width=col_widths[3], anchor="e").grid(row=row_num, column=3, sticky="nsew")

    if not recent_expenses:
        tk.Label(recent_frame, text="No transactions found.", font=("Arial", 12, "italic"), 
                 bg="#FFFFFF", fg="#6C757D", pady=15, padx=10).grid(row=1, column=0, columnspan=4)