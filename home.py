import tkinter as tk
from tkinter import messagebox

password='monomatrix'

pass_win = tk.Tk()
pass_win.title("Password Window")
pass_win.geometry('400x100')

f = open('./password.txt', 'r',encoding="utf-8")
check= f.readline()  # 1行分だけよみこみlineに文字列を代入
check=int(check)
f.close()


def check_open():
    entered_pass = pass_entry.get()
    if password == entered_pass:
        with open('./password.txt', 'w', encoding="utf-8") as f:
            f.write('1')
            pass_win.destroy()
    else:
        messagebox.showerror('Password Error', 'パスワードが異なります')

if check==0:
    pass_label = tk.Label(pass_win, text="パスワードを入力してください", font=("", 10))
    pass_label.pack(side='top',pady=10)
    pass_entry = tk.Entry(pass_win, font=("", 15), bg='lightblue')
    pass_entry.pack(side='top')
    pass_button = tk.Button(pass_win, text='OK', font=("", 15), command=check_open)
    pass_button.pack(side='top', pady=10)
    pass_win.mainloop()

pass_win.destroy()
import mono_matrix
mono_matrix.start()


