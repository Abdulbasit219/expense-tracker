import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def safe_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def calculate_summary(expenses):
    """expenses: list of (id, Description, Amount, Category, DateTime)"""
    total = sum(item[2] for item in expenses)
    categories = {}
    for _, _, amt, cat, _ in expenses:
        categories[cat] = categories.get(cat, 0.0) + safe_float(amt)
    return total, categories

def plot_in_frame(parent_frame, categories):

    for w in parent_frame.winfo_children():
        w.destroy()

    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=100)
    fig.patch.set_facecolor("#222222")  # dark bg for matplotlib
    if categories:
        labels = list(categories.keys())
        values = [categories[k] for k in labels]
        ax.bar(labels, values, color="#1abc9c")
        ax.set_title("Category Spending", color="white", fontsize=10)
        ax.tick_params(axis='x', rotation=20, labelsize=8, colors="white")
        ax.tick_params(axis='y', labelsize=8, colors="white")
        ax.set_ylabel("PKR", color="white", fontsize=9)
    else:
        ax.text(0.5, 0.5, "No Data", ha="center", va="center", color="white", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

def time_based_summary(expenses):
    now = datetime.now()
    one_week = now - timedelta(days=7)
    one_month = now - timedelta(days=30)
    weekly = 0.0
    monthly = 0.0
    for _, _, amt, _, dt in expenses:
        try:
            date_part = dt[:19]  # 'YYYY-MM-DD HH:MM:SS'
            d = datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
            if d >= one_week:
                weekly += safe_float(amt)
            if d >= one_month:
                monthly += safe_float(amt)
        except Exception:
            continue
    return weekly, monthly

def render(root, go_add_callback, go_view_callback, expenses, accent_color):
    # Clear
    for w in root.winfo_children():
        w.destroy()

    top_frame = ctk.CTkFrame(root, fg_color="transparent")
    top_frame.pack(fill="x", padx=16, pady=(12,8))

    title = ctk.CTkLabel(top_frame, text="Dashboard Overview", font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(side="left", padx=(6,0))

    action_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    action_frame.pack(side="right")

    btn_add = ctk.CTkButton(action_frame, text="+ Add New", fg_color=accent_color, command=go_add_callback)
    btn_add.pack(side="right", padx=8)
    btn_view = ctk.CTkButton(action_frame, text="View All", fg_color="transparent", border_color=accent_color, command=go_view_callback)
    btn_view.pack(side="right", padx=8)

    # stats area
    total, categories = calculate_summary(expenses)
    weekly, monthly = time_based_summary(expenses)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.pack(fill="x", padx=16, pady=(8,12))

    left_card = ctk.CTkFrame(stats_frame, width=320, height=140)
    left_card.pack(side="left", padx=(0,12), pady=6)
    left_card.pack_propagate(False)
    ctk.CTkLabel(left_card, text="Total Expense", font=ctk.CTkFont(size=12)).pack(anchor="nw", padx=12, pady=(10,0))
    ctk.CTkLabel(left_card, text=f"PKR {total:,.2f}", font=ctk.CTkFont(size=26, weight="bold"), text_color="#ff6b6b").pack(anchor="nw", padx=12, pady=(6,0))

    right_card = ctk.CTkFrame(stats_frame)
    right_card.pack(side="left", fill="x", expand=True, padx=(0,12))
    right_card_inner = ctk.CTkFrame(right_card, fg_color="transparent")
    right_card_inner.pack(fill="both", expand=True, padx=12, pady=8)

    ctk.CTkLabel(right_card_inner, text=f"Weekly: PKR {weekly:,.2f}", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=6)
    ctk.CTkLabel(right_card_inner, text=f"Monthly: PKR {monthly:,.2f}", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=6)


    viz_frame = ctk.CTkFrame(root)
    viz_frame.pack(fill="both", expand=False, padx=16, pady=(8,12))

    breakdown = ctk.CTkFrame(viz_frame, width=420)
    breakdown.pack(side="left", fill="both", expand=False, padx=(0,12))
    breakdown.pack_propagate(False)
    ctk.CTkLabel(breakdown, text="Spending Breakdown", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", padx=10, pady=(8,4))


    for cat, amt in categories.items():
        row = ctk.CTkFrame(breakdown, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=6)
        ctk.CTkLabel(row, text=cat, anchor="w").pack(side="left", padx=(4,0))
        ctk.CTkLabel(row, text=f"PKR {amt:,.0f}", anchor="e").pack(side="right", padx=(0,10))

    chart_holder = ctk.CTkFrame(viz_frame)
    chart_holder.pack(side="right", fill="both", expand=True)
    plot_in_frame(chart_holder, categories)


    recent_frame = ctk.CTkFrame(root)
    recent_frame.pack(fill="both", expand=True, padx=16, pady=(12,16))

    ctk.CTkLabel(recent_frame, text="Recent Transactions", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", padx=8, pady=(8,6))

    scroll = ctk.CTkScrollableFrame(recent_frame, height=250)
    scroll.pack(fill="both", expand=True, padx=8, pady=(0,8))


    recent = sorted(expenses, key=lambda x: x[4], reverse=True)[:6]
    if not recent:
        ctk.CTkLabel(scroll, text="No transactions yet", text_color="#95a5a6").pack(pady=12)
    else:
        for r in recent:
            fid, desc, amt, cat, dt = r
            card = ctk.CTkFrame(scroll, fg_color="#2b2b2b", corner_radius=6)
            card.pack(fill="x", pady=6, padx=6)
            left = ctk.CTkLabel(card, text=f"{desc}", anchor="w")
            left.pack(side="left", padx=12, pady=10)
            mid = ctk.CTkLabel(card, text=f"{cat} • {dt[:10]}", anchor="w", text_color="#95a5a6")
            mid.pack(side="left", padx=6)
            right = ctk.CTkLabel(card, text=f"PKR {amt:,.2f}", anchor="e", text_color="#ff6b6b", font=ctk.CTkFont(size=12, weight="bold"))
            right.pack(side="right", padx=12)