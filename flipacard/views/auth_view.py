import flet as ft
from src.templates import *
import mysql.connector
import pickle as p

class auth_view():
    def __init__(self):
        self.username = ft.TextField()
        self.password = ft.TextField()
        self.conform = ft.TextField()
        self.login = ft.TextButton("Login", on_click=self.on_login)
        self.signup = ft.TextButton("Sign Up" , on_click=self.on_signup)
        self.con, self.c = connect_to_db()
    
    def on_login(self, e):
        #here u need to verify with the database using connector , cursor , feethc and shit
        uname = self.username.value
        passwd = self.password.value
        ql= f"SELECT * FROM users WHERE uname='{uname}' and passwd='{passwd}'"
        self.c.execute(ql)
        
        try:
            dat = self.c.fetchone()
            print(dat)
            self.save_auth_dat(dat[0], dat[1])

        except mysql.connector.Error as er:
            print(er)
            print(f"login data not found with {uname} with the given password ")

        e.page.go("/home")



    def on_signup(self,e):
        uname = self.username.value
        passwd = self.password.value
        conf = self.conform.value

        if passwd == conf:
            ql = f"INSERT INTO users(uname, passwd) values('{uname}','{passwd}')"
            self.c.execute(ql)
            self.c.execute(f"SELECT * FROM users WHERE uname='{uname}' and passwd='{passwd}'")
            data = self.c.fetchone()
            self.save_auth_dat(data[0], data[1])

        else:
            print("passwords do not match ")
        
        self.con.commit()
        self.con.close()
        e.page.go("/home")

    def save_auth_dat(self, uid, name):
        with open("auth.dat", "wb") as f:
            dat = {"uid":uid, "uname":name}
            p.dump(dat,f)
        
    def build_login(self, e):
        self.con, self.c = connect_to_db()

        return ft.View(route="/login",controls=[self.username, self.password, self.login])

    def build_signup(self, e):
        self.con, self.c = connect_to_db()

        return ft.View(route="/signup",controls=[self.username, self.password, self.conform, self.signup])

    

