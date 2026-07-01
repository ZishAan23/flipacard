import flet as ft
from src.templates import *
import pickle as p

class home_view:
    def __init__(self):
        self.deck_list_ui = ft.ListView()
        self.deck_list = []
        self.selected_deck_index = 0
        self.creator_view_btn = ft.TextButton("Create new deck", on_click=self.on_creator_click)
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
    
    def build(self, e):
        self.init_deck_list()
        e.page.update()
        return ft.View(route="/home", controls=[self.deck_list_ui, self.creator_view_btn])
