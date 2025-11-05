# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from services import (
    create_account, deposit, withdraw, transfer, modify,
    close_account, statement, MIN_OPENING, MIN_BALANCE, INTEREST_RATES_PUBLIC
)
from repo import list_accounts, search_accounts, get_account

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Management System")
        self.geometry("980x620")
        self.minsize(900, 580)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Top Nav
        nav = ttk.Frame(self, padding=10)
        nav.pack(side=tk.TOP, fill=tk.X)

        self.frames = {}
        for (text, cls) in [
            ("Accounts", AccountsFrame),
            ("Create", CreateAccountFrame),
            ("Deposit/Withdraw", CashFrame),
            ("Transfer", TransferFrame),
            ("Modify/Close", ModifyCloseFrame),
            ("Statement", StatementFrame),
            ("About", AboutFrame),
        ]:
            btn = ttk.Button(nav, text=text, command=lambda c=cls: self.show_frame(c))
            btn.pack(side=tk.LEFT, padx=5)

        # Container
        container = ttk.Frame(self, padding=10)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Initialize frames
        for F in (AccountsFrame, CreateAccountFrame, CashFrame, TransferFrame, ModifyCloseFrame, StatementFrame, AboutFrame):
            frame = F(parent=container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.show_frame(AccountsFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

# -------- Frames --------
class AccountsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        hdr = ttk.Label(self, text="All Accounts", font=("Segoe UI", 14, "bold"))
        hdr.pack(anchor="w", pady=(0,10))

        top = ttk.Frame(self)
        top.pack(fill=tk.X)
        self.search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        ttk.Button(top, text="Search", command=self.do_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)

        cols = ("acc_no","name","type","balance","created_at")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=140 if c != "name" else 220, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.footer = ttk.Label(self, text="", anchor="w")
        self.footer.pack(fill=tk.X)

        self.refresh()

    def on_show(self):
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = list_accounts()
        for a in rows:
            self.tree.insert("", tk.END, values=(a.acc_no, a.name, a.type, a.balance, a.created_at))
        self.footer.config(text=f"Total accounts: {len(rows)}")

    def do_search(self):
        q = self.search_var.get().strip()
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = search_accounts(q) if q else list_accounts()
        for a in rows:
            self.tree.insert("", tk.END, values=(a.acc_no, a.name, a.type, a.balance, a.created_at))
        self.footer.config(text=f"Matches: {len(rows)}")

class CreateAccountFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Create New Account", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))
        form = ttk.Frame(self)
        form.pack(anchor="w")

        self.name = tk.StringVar()
        self.typ = tk.StringVar(value="S")
        self.opening = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.name, width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(form, text="Type").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Combobox(form, textvariable=self.typ, values=["S","C"], state="readonly", width=5).grid(row=1, column=1, sticky="w")

        ttk.Label(form, text=f"Opening (>= S:{MIN_OPENING['S']} / C:{MIN_OPENING['C']})").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.opening, width=15).grid(row=2, column=1, sticky="w")

        ttk.Button(self, text="Create", command=self.submit).pack(pady=10)

        self.msg = ttk.Label(self, text="", foreground="green")
        self.msg.pack(anchor="w")

    def submit(self):
        try:
            name = self.name.get().strip()
            typ = self.typ.get().strip().upper()
            opening = int(self.opening.get().strip())
            acc_no = create_account(name, typ, opening)
            self.msg.config(text=f"Account created: {acc_no}")
            self.name.set(""); self.opening.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class CashFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Deposit / Withdraw", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        form = ttk.Frame(self); form.pack(anchor="w")
        self.acc = tk.StringVar()
        self.amount = tk.StringVar()

        ttk.Label(form, text="Account No").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.acc, width=15).grid(row=0, column=1, sticky="w")

        ttk.Label(form, text="Amount").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.amount, width=15).grid(row=1, column=1, sticky="w")

        btns = ttk.Frame(self); btns.pack(anchor="w", pady=10)
        ttk.Button(btns, text="Deposit", command=self.do_deposit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Withdraw", command=self.do_withdraw).pack(side=tk.LEFT, padx=5)

        self.info = ttk.Label(self, text="", foreground="green")
        self.info.pack(anchor="w")

    def do_deposit(self):
        try:
            acc = int(self.acc.get())
            amt = int(self.amount.get())
            deposit(acc, amt)
            bal = get_account(acc).balance
            self.info.config(text=f"Deposited {amt}. New balance: {bal}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_withdraw(self):
        try:
            acc = int(self.acc.get())
            amt = int(self.amount.get())
            withdraw(acc, amt)
            bal = get_account(acc).balance
            self.info.config(text=f"Withdrawn {amt}. New balance: {bal}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class TransferFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Transfer", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        form = ttk.Frame(self); form.pack(anchor="w")
        self.src = tk.StringVar()
        self.dst = tk.StringVar()
        self.amt = tk.StringVar()

        ttk.Label(form, text="From Acc").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.src, width=15).grid(row=0, column=1, sticky="w")

        ttk.Label(form, text="To Acc").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.dst, width=15).grid(row=1, column=1, sticky="w")

        ttk.Label(form, text="Amount").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.amt, width=15).grid(row=2, column=1, sticky="w")

        ttk.Button(self, text="Transfer", command=self.do_transfer).pack(pady=10)

        self.note = ttk.Label(self, text="", foreground="green")
        self.note.pack(anchor="w")

    def do_transfer(self):
        try:
            src = int(self.src.get()); dst = int(self.dst.get()); amt = int(self.amt.get())
            transfer(src, dst, amt)
            sbal = get_account(src).balance
            self.note.config(text=f"Transferred {amt} from {src} to {dst}. Src balance: {sbal}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class ModifyCloseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Modify / Close Account", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        form = ttk.Frame(self); form.pack(anchor="w")

        self.acc = tk.StringVar()
        self.name = tk.StringVar()
        self.typ = tk.StringVar()

        ttk.Label(form, text="Account No").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.acc, width=15).grid(row=0, column=1, sticky="w")

        ttk.Label(form, text="New Name").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(form, textvariable=self.name, width=25).grid(row=1, column=1, sticky="w")

        ttk.Label(form, text="New Type [S/C]").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Combobox(form, textvariable=self.typ, values=["", "S", "C"], width=5, state="readonly").grid(row=2, column=1, sticky="w")

        btns = ttk.Frame(self); btns.pack(anchor="w", pady=10)
        ttk.Button(btns, text="Modify", command=self.do_modify).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Close Account", command=self.do_close).pack(side=tk.LEFT, padx=5)

        self.msg = ttk.Label(self, text="", foreground="green")
        self.msg.pack(anchor="w")

    def do_modify(self):
        try:
            acc = int(self.acc.get())
            nm = self.name.get().strip() or None
            tp = self.typ.get().strip() or None
            modify(acc, nm, tp)
            self.msg.config(text="Account updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_close(self):
        from services import close_account
        try:
            acc = int(self.acc.get())
            if not messagebox.askyesno("Confirm", "Close this account?"):
                return
            payout = close_account(acc)
            self.msg.config(text=f"Account closed. Payout: {payout}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class StatementFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Account Statement", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        filt = ttk.Frame(self); filt.pack(anchor="w")
        self.acc = tk.StringVar()
        self.f = tk.StringVar()
        self.t = tk.StringVar()

        ttk.Label(filt, text="Account No").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(filt, textvariable=self.acc, width=15).grid(row=0, column=1, sticky="w")

        ttk.Label(filt, text="From (YYYY-MM-DD)").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(filt, textvariable=self.f, width=15).grid(row=0, column=3, sticky="w")

        ttk.Label(filt, text="To (YYYY-MM-DD)").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Entry(filt, textvariable=self.t, width=15).grid(row=0, column=5, sticky="w")

        ttk.Button(self, text="Load", command=self.load).pack(pady=10, anchor="w")

        cols = ("kind","amount","note","created_at")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, anchor="center", width=160 if c != "note" else 250)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.footer = ttk.Label(self, text="")
        self.footer.pack(anchor="w", pady=5)

    def load(self):
        from services import statement
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            acc = int(self.acc.get())
            rows = statement(acc, self.f.get().strip() or None, self.t.get().strip() or None)
            total_in = 0; total_out = 0
            for k,a,n,dt in rows:
                self.tree.insert("", "end", values=(k, a, n or "", dt))
                if k in ("DEPOSIT","TRANSFER_IN","INTEREST","OPEN"):
                    total_in += a
                elif k in ("WITHDRAW","TRANSFER_OUT"):
                    total_out += a
            bal = get_account(acc).balance if get_account(acc) else 0
            self.footer.config(text=f"Rows: {len(rows)} | In: {total_in} | Out: {total_out} | Current Balance: {bal}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class AboutFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="About", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))
        txt = (
            "Bank Management System (Tkinter + SQLite)\n"
            f"- Min Opening: S:{MIN_OPENING['S']} / C:{MIN_OPENING['C']}\n"
            f"- Min Balance: S:{MIN_BALANCE['S']} / C:{MIN_BALANCE['C']}\n"
            f"- Interest (yearly): S:{int(INTEREST_RATES_PUBLIC['S']*100)}% / C:{int(INTEREST_RATES_PUBLIC['C']*100)}%\n"
            "\nFeatures:\n"
            "• Create accounts • Deposit/Withdraw • Transfer • Modify/Close • Search/Listing • Statements\n"
        )
        ttk.Label(self, text=txt, justify="left").pack(anchor="w")
