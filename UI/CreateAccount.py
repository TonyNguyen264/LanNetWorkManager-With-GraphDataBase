from tkinter import *
from tkinter import messagebox
import subprocess
import os
import ast
import hashlib

def signup_command():

    # log.withdraw()
    window=Tk()
    window.title("")
    window.geometry('500x500+180+150')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def signup():
        username = user.get()
        password = code.get()
        role = 'admin'
        conform_password = conform_code.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        username_infile=[]
        with open("signup_info.txt", "r") as file:
            lines = file.readlines()
        for line in lines:
            parts = line.strip().split(", ")
            username_infile.append(parts[0].replace("Username: ", ""))
        if username in username_infile:
            messagebox.showerror('Invalid',  'Username already exists')
            user.focus_set()
        elif password != conform_password:
            messagebox.showerror('Invalid', 'Both Password should match')
            code.focus_set()
        else:
            try:
                with open("signup_info.txt", "a") as file:
                    file.write(f"Username: {username}, Password: {hashed_password}, Role: {role}\n")

                messagebox.showinfo('Signup', 'Sucessfully sign up')
                window.destroy()

            except:
                messagebox.showerror('Invalid', 'Fail to write data')

        # if password == conform_password and username not in username_infile:
        #     try:
        #         with open("signup_info.txt", "a") as file:
        #             file.write(f"Username: {username}, Password: {password}, Role: {role}\n")
        #
        #         messagebox.showinfo('Signup', 'Sucessfully sign up')
        #
        #     except:
        #         file = open('emtsheet.txt', 'w')
        #         pp = str({'Username': 'password'})
        #         file.write(pp)
        #         file.close()
        #
        # else:
        #     messagebox.showerror('Invalid', 'Both Password should match or username already exists')

    # image setting
    # img = PhotoImage(file='img/create.png')
    # Label(window, image=img, bg='white').place(x=50, y=90)
    frame = Frame(window, width=300, height=400, bg='white')
    frame.place(x=100, y=50)
    # Word Sign in  setting
    heading = Label(frame, text='Create Account', fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
    heading.place(x=20, y=5)

    # username
    # User NAme Setting
    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        if user.get() == '':
            user.insert(0, 'Username')

    # lbl_name = Label(frame, text='Username: ', fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
    # lbl_name.place(x=-40, y=80)

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert('0', 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # password
    def on_enter(e):
        code.delete(0, 'end')
        code.config(fg="black", show="*")  # Thay đổi màu chữ thành đen và hiển thị *

    def on_leave(e):
        if code.get() == '':
            code.insert(0, 'Confirm Password')

    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    # code = Entry(frame, show="*", border=0)
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # conform password


    def on_enter(e):
        conform_code.delete(0, 'end')
        conform_code.config(fg="black", show="*")  # Thay đổi màu chữ thành đen và hiển thị *

    def on_leave(e):
        if conform_code.get() == '':
            conform_code.insert(0, 'Confirm Password')

    conform_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    # conform_code = Entry(frame, show="*", border=0)
    conform_code.place(x=30, y=220)
    conform_code.insert('0', 'Confirm Password')
    conform_code.bind('<FocusIn>', on_enter)
    conform_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    # Button sign in and label

    Button(frame, width=39, pady=7, text='Sign up', bg='black', fg='white', border=0, command=signup).place(x=35, y=280)

    # CreateAccount.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
# log = Tk()
# log.title("SignIn")
# log.geometry('890x500+180+150')
# log.configure(bg='white')
# log.resizable(False, False)
# signup_command()
