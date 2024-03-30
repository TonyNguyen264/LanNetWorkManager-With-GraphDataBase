from tkinter import *
from tkinter import messagebox
import subprocess
import os
import ast
import hashlib

def signup_command(username):

    # log.withdraw()
    window=Tk()
    window.title("")
    window.geometry('500x500+180+150')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def save_user_info(users):
        with open("signup_info.txt", "w") as file:
            for user in users:
                file.write(f"Username: {user['username']}, Password: {user['password']}, Role: {user['role']}\n")

    def load_user_info():
        users = []
        with open("signup_info.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                username = line.split("Username: ")[1].split(",")[0].strip()
                password = line.split("Password: ")[1].split(",")[0].strip()
                role = line.split("Role: ")[1].strip()
                users.append({'username': username, 'password': password, 'role': role})
        return users

    # def signup():
    #     username = old_code.get()
    #     password = code.get()
    #     role = 'amin'
    #     conform_password = conform_code.get()
    #     with open("signup_info.txt", "r") as file:
    #         lines = file.readlines()
    #     for line in lines:
    #         parts = line.strip().split(", ")
    #     username_infile = parts[0].replace("Username: ", "")
    #     if username in username_infile:
    #         messagebox.showerror('Invalid',  'Username already exists')
    #         user.focus_set()
    #     elif password != conform_password:
    #         messagebox.showerror('Invalid', 'Both Password should match')
    #         code.focus_set()
    #     else:
    #         try:
    #             with open("signup_info.txt", "a") as file:
    #                 file.write(f"Username: {username}, Password: {password}, Role: {role}\n")
    #
    #             messagebox.showinfo('Signup', 'Sucessfully sign up')
    #
    #         except:
    #             messagebox.showerror('Invalid', 'Fail to write data')

    def change_password():
        # username = entry_username.get()
        users = load_user_info()
        old_password = old_code.get()
        new_password = code.get()
        confirm_password = conform_code.get()
        # print(user)

        if new_password == confirm_password:
            user_found = False
            hashed_new_password=hashlib.sha256(new_password.encode()).hexdigest()

            for user in users:
                hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()
                if user['username'] == username and user['password'] == hashed_old_password:
                    user['password'] = hashed_new_password
                    save_user_info(users)
                    messagebox.showinfo("Thành công", "Mật khẩu đã được thay đổi và lưu!")
                    window.destroy()
                    user_found = True
                    break

            if not user_found:
                messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu cũ không đúng")
        else:
            messagebox.showerror("Lỗi", "Xác nhận mật khẩu không khớp")

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
    heading = Label(frame, text=username, fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
    heading.place(x=20, y=5)

    # username
    # User NAme Setting
    def on_enter(e):
        old_code.delete(0, 'end')
        old_code.config(fg="black", show="*")  # Thay đổi màu chữ thành đen và hiển thị *

    def on_leave(e):
        if old_code.get() == '':
            old_code.insert(0, 'Confirm Password')
            # entry.insert(0, "Nhập chữ ở đây")
            # entry.config(fg="grey", show="")

    # lbl_name = Label(frame, text='Username: ', fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
    # lbl_name.place(x=-40, y=80)

    old_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    old_code.place(x=30, y=80)
    old_code.insert('0', 'Old Password')
    old_code.bind('<FocusIn>', on_enter)
    old_code.bind('<FocusOut>', on_leave)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # password
    def on_enter(e):
        code.delete(0, 'end')
        code.config(fg="black", show="*")  # Thay đổi màu chữ thành đen và hiển thị *

    def on_leave(e):
        if code.get() == '':
            code.insert(0, 'Password')
            # entry.insert(0, "Nhập chữ ở đây")
            # entry.config(fg="grey", show="")


    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    code.insert(0, 'Password')
    # code = Entry(frame, show="*", border=0)
    code.place(x=30, y=150)
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
            # entry.insert(0, "Nhập chữ ở đây")
            # entry.config(fg="grey", show="")

    conform_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    # conform_code = Entry(frame, show="*", border=0)
    conform_code.place(x=30, y=220)
    conform_code.insert('0', 'Confirm Password')
    conform_code.bind('<FocusIn>', on_enter)
    conform_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    # Button sign in and label

    Button(frame, width=39, pady=7, text='Sign up', bg='black', fg='white', border=0, command=change_password).place(x=35, y=280)




    window.mainloop()
# log = Tk()
# log.title("SignIn")
# log.geometry('890x500+180+150')
# log.configure(bg='white')
# log.resizable(False, False)
