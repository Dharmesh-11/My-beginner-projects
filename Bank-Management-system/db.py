# db.py
import sqlite3
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "bank.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_no INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('S','C')) NOT NULL,
            balance INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_no INTEGER NOT NULL,
            kind TEXT CHECK(kind IN ('DEPOSIT','WITHDRAW','TRANSFER_IN','TRANSFER_OUT','INTEREST','OPEN')) NOT NULL,
            amount INTEGER NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(acc_no) REFERENCES accounts(acc_no)
        )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tx_accno ON transactions(acc_no)")
