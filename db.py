import sqlite3 as sql
from pathlib import Path
from datetime import datetime

DB_DIR = Path("./Output")
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "expense.db"

def connect_db():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Description TEXT NOT NULL,
            Amount REAL NOT NULL,
            Category TEXT NOT NULL,
            DateTime TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_db(desc, amnt, ctgr, dt=None):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    if dt:
        cursor.execute("INSERT INTO Expense (Description, Amount, Category, DateTime) VALUES (?, ?, ?, ?)",
                       (desc, float(amnt), ctgr, dt))
    else:
        cursor.execute("INSERT INTO Expense (Description, Amount, Category) VALUES (?, ?, ?)",
                       (desc, float(amnt), ctgr))
    conn.commit()
    cursor.close()
    conn.close()

def update_db(desc, amnt, ctgr, e_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE Expense SET Description = ?, Amount = ?, Category = ? WHERE id = ?",
                   (desc, float(amnt), ctgr, e_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_db(e_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Expense WHERE id = ?", (e_id,))
    conn.commit()
    cursor.close()
    conn.close()

def load_all_expenses():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, Description, Amount, Category, DateTime FROM Expense")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    normalized = []
    for r in rows:
        dt = r[4]
        if dt is None:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        normalized.append((r[0], r[1], float(r[2]), r[3], str(dt)))
    return normalized