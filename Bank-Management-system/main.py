# main.py
from db import init_db
from gui import BankApp

def main():
    init_db()
    app = BankApp()
    app.mainloop()

if __name__ == "__main__":
    main()
