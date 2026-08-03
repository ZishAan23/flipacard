import flet as ft
from src.templates import *
import pickle as p

class home_view:
    def __init__(self):
        self.deck_list_ui = ft.ListView()
        self.deck_list = []
        self.selected_deck_index = 0
        self.creator_view_btn = ft.TextButton("Create new deck", on_click=self.on_creator_click)
        self.sign_up_dlg = ft.AlertDialog(content=ft.Text("Please either login or sign up to be able to use online features "), actions=[ft.TextButton("Login", on_click=self.login_btn), ft.TextButton("Sign up", on_click=self.sign_up_btn)])
        self.online_view_btn = ft.TextButton("Browse Online flashcards", on_click=self.on_online_click)
        for i in find_deck_files_in("./decks"):
            self.deck_list.append(i)
            self.deck_list_ui.controls.append(ft.Container(content=ft.TextButton(i, on_click=self.on_deck_click)))
        
    def init_deck_list(self):
        self.deck_list_ui.controls.clear()
        self.deck_list = []
        for i in find_deck_files_in("./decks"):
            self.deck_list.append(i)
            self.deck_list_ui.controls.append(ft.Container(content=ft.TextButton(i, on_click=self.on_deck_click)))
        

    def on_creator_click(self, e):
        e.page.go("/creator")

    def on_deck_click(self, e):
        j=0
        for i in self.deck_list_ui.controls:
            if i==e.control.parent:
                self.selected_deck_index=j
                break
            j+=1
        
        with open(self.deck_list[self.selected_deck_index], "rb") as f:
            deck_obj = p.load(f)
        
        e.page.session.store.set("selected_deck", deck_obj)
        e.page.update()
        e.page.go("/practice")
    
    def login_btn(self, e):
        e.page.go("/login")
        self.close_auth_dlg(e)
    
    def sign_up_btn(self, e):
        e.page.go("/signup")
        self.close_auth_dlg(e)

    def close_auth_dlg(self, e):
        self.sign_up_dlg.open =False
        e.page.dialog = None
        e.page.update()

    def on_online_click(self,e):
        e.page.go("/browse")
        e.page.update()
        

    def build(self, e):
        self.init_deck_list()

        with open("auth.dat", "rb") as f:
            try :
                auth_data = p.load(f)
                e.page.session.store.set("uid", auth_data["uid"])
                e.page.session.store.set("uname", auth_data["uname"])
            except:
                add_to_overlay(e.page, self.sign_up_dlg)
                e.page.dialog = self.sign_up_dlg
                self.sign_up_dlg.open = True
                e.page.update()           

        e.page.update()
        return ft.View(route="/home", controls=[self.deck_list_ui, self.creator_view_btn, self.online_view_btn])
