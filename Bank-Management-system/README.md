# 🏦 Bank Management System  
**Python + Tkinter + SQLite Desktop Application**

This project is a **Graphical Bank Management System** that allows the user to maintain and manage bank accounts.  
It provides an easy-to-use Tkinter-based GUI and stores all account records securely using SQLite (no external server needed).

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| **Create New Account** | Add customers with Saving or Current account type |
| **Deposit & Withdraw** | Perform safe cash transactions |
| **Fund Transfer** | Transfer money between two accounts |
| **Search Accounts** | Search by Name or Account Number |
| **View All Accounts** | Displays accounts in a sortable table |
| **Modify Account Details** | Update account holder name or account type |
| **Close Account** | Automatically processes funds & removes account |
| **Transaction History / Statement** | View detailed account transactions between specific dates |
| **Local Database (SQLite)** | No internet / external DB setup required |
| **User-Friendly UI** | Simple and clean Tkinter interface |

## 🖥️ Screenshots (Add your own)
| Account List | Create Account |
|-------------|----------------|
| *Add image* | *Add image* |

## 🛠 Technology Stack

| Component | Technology |
|----------|------------|
| GUI | Tkinter |
| Database | SQLite |
| Language | Python 3.x |
| Pattern | Layered Architecture (GUI → Service → Repository → DB) |

## 🗂 Project Structure

```
bank_app/
├─ main.py            # Application entry point
├─ gui.py             # Tkinter UI windows & screens
├─ services.py        # Business logic (deposit, withdraw, transfer, etc.)
├─ repo.py            # Database operations (CRUD)
├─ db.py              # Database initialization (tables setup)
└─ models.py          # Data models (Account, Transaction)
```

## 🔧 Requirements

| Requirement | Details |
|------------|---------|
| Python Version | Python 3.7+ |
| Tkinter | Included with Python |
| SQLite | Included with Python |

## 🚀 How to Run

```
cd bank_app
python main.py     # Windows
python3 main.py    # macOS / Linux
```

## 📊 Banking Rules

| Account Type | Min Opening Balance | Min Maintain Balance | Interest |
|-------------|--------------------|----------------------|----------|
| Saving (S)  | ₹500               | ₹500                | 3% yearly |
| Current (C) | ₹1000              | ₹1000               | No interest |

## 💾 Database File

Data is stored in:
```
bank.db
```

## 🧱 Future Enhancements
- Login System (Admin/User)
- PDF Export for Statements
- Modern UI with CustomTkinter
- Convert to EXE Installer

## 👨‍💻 Author
Your Name Here

