# services.py
from typing import Optional
from repo import (
    get_account, list_accounts, search_accounts, create_account as repo_create,
    update_account_meta, delete_account, set_balance, add_tx, get_statement
)

MIN_OPENING = {"S": 500, "C": 1000}
MIN_BALANCE = {"S": 500, "C": 1000}
INTEREST_RATES = {"S": 0.03, "C": 0.00}  # yearly simple
# Expose for GUI tables
INTEREST_RATES_PUBLIC = INTEREST_RATES

def create_account(name: str, typ: str, opening: int) -> int:
    typ = typ.upper()
    if typ not in ("S", "C"):
        raise ValueError("Account type must be S or C")
    if opening < MIN_OPENING[typ]:
        raise ValueError(f"Opening must be >= {MIN_OPENING[typ]}")
    return repo_create(name, typ, opening)

def deposit(acc_no: int, amount: int):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    acc = get_account(acc_no)
    if not acc:
        raise ValueError("Account not found")
    new_bal = acc.balance + amount
    set_balance(acc_no, new_bal)
    add_tx(acc_no, "DEPOSIT", amount)

def withdraw(acc_no: int, amount: int):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    acc = get_account(acc_no)
    if not acc:
        raise ValueError("Account not found")
    if acc.balance - amount < MIN_BALANCE[acc.type]:
        raise ValueError(f"Withdrawal would breach minimum balance ({MIN_BALANCE[acc.type]})")
    new_bal = acc.balance - amount
    set_balance(acc_no, new_bal)
    add_tx(acc_no, "WITHDRAW", amount)

def transfer(src: int, dst: int, amount: int):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if src == dst:
        raise ValueError("Cannot transfer to same account")
    s = get_account(src)
    d = get_account(dst)
    if not s or not d:
        raise ValueError("Source or destination account not found")
    if s.balance - amount < MIN_BALANCE[s.type]:
        raise ValueError(f"Transfer would breach source minimum balance ({MIN_BALANCE[s.type]})")
    set_balance(src, s.balance - amount)
    set_balance(dst, d.balance + amount)
    add_tx(src, "TRANSFER_OUT", amount, f"to {dst}")
    add_tx(dst, "TRANSFER_IN", amount, f"from {src}")

def modify(acc_no: int, name: Optional[str], typ: Optional[str]):
    acc = get_account(acc_no)
    if not acc:
        raise ValueError("Account not found")
    new_name = name.strip() if name else acc.name
    new_type = (typ or acc.type).upper()
    if new_type not in ("S","C"):
        raise ValueError("Type must be S or C")
    # enforce min balance when switching type
    if acc.balance < MIN_BALANCE[new_type]:
        raise ValueError(f"Balance {acc.balance} below minimum for {new_type} ({MIN_BALANCE[new_type]})")
    update_account_meta(acc_no, new_name, new_type)

def close_account(acc_no: int) -> int:
    acc = get_account(acc_no)
    if not acc:
        raise ValueError("Account not found")
    payout = acc.balance
    if payout > 0:
        add_tx(acc_no, "WITHDRAW", payout, "Account closure payout")
    delete_account(acc_no)
    return payout

def statement(acc_no: int, date_from: Optional[str], date_to: Optional[str]):
    if not get_account(acc_no):
        raise ValueError("Account not found")
    return get_statement(acc_no, date_from, date_to)
