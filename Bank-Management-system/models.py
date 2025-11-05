# models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Account:
    acc_no: int
    name: str
    type: str  # 'S' or 'C'
    balance: int
    created_at: str

@dataclass
class Transaction:
    acc_no: int
    kind: str       # DEPOSIT/WITHDRAW/TRANSFER_IN/TRANSFER_OUT/INTEREST/OPEN
    amount: int
    note: Optional[str]
    created_at: str
