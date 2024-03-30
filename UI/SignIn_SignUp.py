from tkinter import *
from tkinter import messagebox
import subprocess
import os
import ast
import hashlib
#  Window app
def show_login():
    log = Tk()
    log.title("SignIn")
    log.geometry('890x500+180+150')
    log.configure(bg='white')
    log.resizable(False, False)

    usernameDN = ' '
    roleDN = ' '


    def get_user_role():
        return usernameDN, roleDN


    def signin():
        username = user_entry.get()
        password = code.get()



        users = []
        with open("signup_info.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                username_infile = line.split("Username: ")[1].split(",")[0].strip()
                password_infile = line.split("Password: ")[1].split(",")[0].strip()
                role = line.split("Role: ")[1].strip()
                users.append({'username': username_infile, 'password': password_infile, 'role': role})

        # print(role)
        # user_accounts.append({"username": username, "password": password,"role": role})
        # print(username, password)
        user_found = ''
        for user in users:
            # print(user)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user['username'] == username and user['password'] == hashed_password and user['role']=='user':
                 user_found='user'
            elif user['username'] == username and user['password'] == hashed_password and user['role']=='admin':
                user_found='admin'

        if user_found=='user':
            usernameDN = username
            role = user_found
            import FormUserPC
            log.withdraw()
            log.destroy()
            FormUserPC.show_form_admin(usernameDN,role)
            # PageUser.show_form_admin_switch(username, role)
            # return username,role

        elif user_found == 'admin':
            username = username
            role = user_found
            import FormAdminPC
            log.withdraw()
            log.destroy()
            FormAdminPC.show_form_admin(username,role)
            # return username,role



            # log.withdraw()
            # log.destroy()
            # result_label.config(text="Đăng nhập thành công!")
        else:
            messagebox.showerror('Invalid', 'invalid username or password')

        # if username in r.keys() and password==r[username]:
        #
        #
        #
        #
        #
        #
        # else:
        #   messagebox.showerror('Invalid','invalid username or password')


    def open_new_window():
        screen = Toplevel(log)
        screen.title("App")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")
        # secongui.create_second_gui()
        Label(screen, text='Vao trang chinh', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
        screen.mainloop()


    # Screen 2
    def signup_command():
        window = Toplevel(log)
        window.title("")
        window.geometry('925x500+180+150')
        window.configure(bg='#fff')
        window.resizable(False, False)

        def signup():
            username = user_entry.get()
            password = code.get()
            role = 'user'
            conform_password = conform_code.get()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            username_infile = []
            with open("signup_info.txt", "r") as file:
                lines = file.readlines()
            for line in lines:
                parts = line.strip().split(", ")
                username_infile.append(parts[0].replace("Username: ", ""))
            if username in username_infile:
                messagebox.showerror('Invalid', 'Username already exists')
                user_entry.focus_set()
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

                    # file=open('emtsheet.txt','r+')
                    # d = file.read()
                    # r=ast.literal_eval(d)
                    # dict2 = {username:password}
                    # r.update(dict2)
                    # file.truncate(0)
                    # file.close()
                    # file=open('emtsheet.txt','w')
                    # w = file.write(str(r))
                    messagebox.showinfo('Signup', 'Sucessfully sign up')



        def sign():
            window.destroy()

        # image setting
        img = PhotoImage(file='img/sign.png')
        Label(window, image=img, bg='white').place(x=50, y=90)
        frame = Frame(window, width=350, height=390, bg='white')
        frame.place(x=480, y=50)
        # Word Sign in  setting
        heading = Label(frame, text='Sign Up', fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
        heading.place(x=20, y=5)

        # username
        # User NAme Setting
        def on_enter(e):
            user_entry.delete(0, 'end')

        def on_leave(e):
            if user_entry.get() == '':
                user_entry.insert(0, 'Username')

        user_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        user_entry.place(x=30, y=80)
        user_entry.insert('0', 'Username')
        user_entry.bind('<FocusIn>', on_enter)
        user_entry.bind('<FocusOut>', on_leave)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        # password
        def on_enter(e):
            code.delete(0, 'end')

        def on_leave(e):
            if code.get() == '':
                code.insert(0, 'Password')

        code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        code = Entry(frame, show="*", border=0)
        code.place(x=30, y=150)
        code.insert('0', 'Password')
        code.bind('<FocusIn>', on_enter)
        code.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        # conform password
        def on_enter(e):
            conform_code.delete(0, 'end')

        def on_leave(e):
            if conform_code.get() == '':
                conform_code.insert(0, 'Confirm Password')

        conform_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        conform_code = Entry(frame, show="*", border=0)
        conform_code.place(x=30, y=220)
        conform_code.insert('0', 'Confirm Password')
        conform_code.bind('<FocusIn>', on_enter)
        conform_code.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

        # Button sign in and label

        Button(frame, width=39, pady=7, text='Sign up', bg='black', fg='white', border=0, command=signup).place(x=35, y=280)
        label = Label(frame, text="I have an account", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=340)

        sign_in = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='black', command=sign)

        sign_in.place(x=200, y=340)

        window.mainloop()


    # Set Image
    img = PhotoImage(file='img/login.png')
    Label(log, image=img, bg='white').place(x=10, y=10)

    frame = Frame(log, width=350, height=350, bg='white')
    frame.place(x=480, y=70)

    # Word Sign in  setting
    heading = Label(frame, text='Sign In', fg='black', bg='white', font=('Microsoft YaHei UI Light', 19, 'bold'))
    heading.place(x=20, y=5)


    # User NAme Setting
    def on_enter(e):
        user_entry.delete(0, 'end')


    def on_leave(e):
        name = user_entry.get()
        if name == '':
            user_entry.insert(0, 'Username')


    user_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user_entry.place(x=30, y=80)
    user_entry.insert('0', 'Username')
    user_entry.bind('<FocusIn>', on_enter)
    user_entry.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


    # password Setting
    def on_enter(e):
        code.delete(0, 'end')


    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')


    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    code = Entry(frame, show="*", border=0)
    code.place(x=30, y=150)
    code.insert('0', 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # Button sign in and label

    Button(frame, width=39, pady=7, text='Sign in', bg='black', fg='white', border=0, command=signin).place(x=35, y=204)
    label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 11))
    label.place(x=50, y=270)
    if True:
        # log.close
        sign_up = Button(frame, width=5, text='Sign up', border=0, bg='white', cursor='hand2', fg='black',
                         command=signup_command)

    sign_up.place(x=215, y=270)

    log.mainloop()

