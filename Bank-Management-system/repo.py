# repo.py
from typing import List, Optional, Tuple
from datetime import datetime
from db import get_conn
from models import Account

DATE_FMT = "%Y-%m-%d %H:%M:%S"

def next_acc_no() -> int:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(acc_no)+1, 100001) FROM accounts")
        return int(cur.fetchone()[0])

def get_account(acc_no: int) -> Optional[Account]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT acc_no,name,type,balance,created_at FROM accounts WHERE acc_no=?", (acc_no,))
        row = cur.fetchone()
        if row:
            return Account(*row)
        return None

def list_accounts() -> List[Account]:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT acc_no,name,type,balance,created_at FROM accounts ORDER BY acc_no")
        return [Account(*r) for r in cur.fetchall()]

def search_accounts(query: str) -> List[Account]:
    with get_conn() as conn:
        cur = conn.cursor()
        if query.isdigit():
            cur.execute("SELECT acc_no,name,type,balance,created_at FROM accounts WHERE acc_no=?", (int(query),))
        else:
            cur.execute("SELECT acc_no,name,type,balance,created_at FROM accounts WHERE name LIKE ?", (f"%{query}%",))
        return [Account(*r) for r in cur.fetchall()]

def create_account(name: str, typ: str, opening: int) -> int:
    now = datetime.now().strftime(DATE_FMT)
    with get_conn() as conn:
        cur = conn.cursor()
        acc_no = next_acc_no()
        cur.execute(
            "INSERT INTO accounts(acc_no,name,type,balance,created_at) VALUES(?,?,?,?,?)",
            (acc_no, name, typ, opening, now)
        )
        cur.execute(
            "INSERT INTO transactions(acc_no,kind,amount,note,created_at) VALUES(?,?,?,?,?)",
            (acc_no, "OPEN", opening, "Opening balance", now)
        )
        return acc_no

def update_account_meta(acc_no: int, name: str, typ: str) -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET name=?, type=? WHERE acc_no=?", (name, typ, acc_no))

def delete_account(acc_no: int) -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE acc_no=?", (acc_no,))

def set_balance(acc_no: int, new_balance: int) -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET balance=? WHERE acc_no=?", (new_balance, acc_no))

def add_tx(acc_no: int, kind: str, amount: int, note: Optional[str] = None) -> None:
    now = datetime.now().strftime(DATE_FMT)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions(acc_no,kind,amount,note,created_at) VALUES(?,?,?,?,?)",
            (acc_no, kind, amount, note, now)
        )

def get_statement(acc_no: int, date_from: Optional[str], date_to: Optional[str]) -> List[Tuple]:
    q = "SELECT kind,amount,note,created_at FROM transactions WHERE acc_no=?"
    params = [acc_no]
    if date_from:
        q += " AND date(created_at) >= date(?)"
        params.append(date_from)
    if date_to:
        q += " AND date(created_at) <= date(?)"
        params.append(date_to)
    q += " ORDER BY datetime(created_at)"
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(q, tuple(params))
        return cur.fetchall()
