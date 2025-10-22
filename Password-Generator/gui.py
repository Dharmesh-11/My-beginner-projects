import tkinter as tk
from tkinter import messagebox
from logic import generate_password

def on_generate():
    try:
        length = int(length_entry.get())
        password = generate_password(length)
        result_var.set(password)
    except ValueError as e:
        messagebox.showerror("Error",str(e))
        
        
#Gui setup

root = tk.Tk()
root.title("Password Gnerator")
root.geometry("400x200")
root.config(padx=20,pady=20)

#widget

tk.Label(root,text="Enter Password Length:",font=('Arial',12)).pack(pady=5)
length_entry = tk.Entry(root,width=10,font=('Arial',12))
length_entry.pack()

tk.Button(root,text = "Generate Password", font=('Arial',12),command=on_generate).pack(pady=10)

result_var = tk.StringVar()
result_label = tk.Label(root,textvariable=result_var,font=('Courier',14,'bold'),fg="blue")
result_label.pack(pady=10)

root.mainloop()