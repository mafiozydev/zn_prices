import sqlite3
from datetime import datetime

DB_NAME = "prices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        title TEXT,
        price_rub REAL,
        old_price_rub REAL,
        discount_percent INTEGER,
        scraped_at TEXT
    )''')
    conn.commit()
    conn.close()

def save_product(url, title, price_rub, old_price_rub=None, discount_percent=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO prices (url, title, price_rub, old_price_rub, discount_percent, scraped_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (url, title, price_rub, old_price_rub, discount_percent, datetime.now().isoformat()))
    conn.commit()
    conn.close()