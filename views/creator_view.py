import flet as ft
from src.templates import *
import pickle as p
import time

class creator_view:

    def __init__(self):
        self.deck = Deck("", [])
        self.card_list = ft.ListView(spacing=10)
        self.question_field = ft.TextField()
        self.answer_field = ft.TextField()
        self.add_card_button = ft.ElevatedButton("Add Card", on_click=self.add_card, expand=True)
        self.save_deck = ft.ElevatedButton("Save Deck", on_click=self.save_deck, expand=True)
        self.del_card_btn = ft.ElevatedButton("Delete Card", on_click=self.delete_card, expand=True, visible=False)

        self.empty_dlg = ft.AlertDialog(content=ft.Text("Please fill in both fields"), actions=[ft.TextButton("OK", on_click=self.on_close_empty_dlg)])
        self.selected_card_index = -1
        self.selected_deck_path = ""
        
        self.new_deck_btn = ft.Button(content="New Deck", on_click=self.init_new_deck)
        self.load_deck_btn = ft.Button(content="Edit old deck", on_click=self.load_deck)
        self.init_dialog = ft.AlertDialog(content=ft.Text("create a new deck or edit a alreaedy made one"), actions=[self.new_deck_btn, self.load_deck_btn])
        self.select_deck_dlg = ft.FilePicker() #no intialise it in both places as well just update the page when u r builiding so that file picker can connect with the app
    

    def init_new_deck(self, e):
        self.deck = Deck("", [])
        self.card_list.controls.clear()
        self.selected_card_index = -1
        self.init_dialog.open = False
        e.page.update()

    async def load_deck(self, e):
        #remove the init dialog
        self.init_dialog.open = False
        e.page.update()

        #start the file picker dialog box
        result = await self.select_deck_dlg.pick_files(allowed_extensions=["fc"])
        if result:
            self.import_deck(result, e)
    
    async def save_deck(self, e):
        result = await self.select_deck_dlg.save_file(allowed_extensions=["fc"], file_name=".fc")
        if result:
            self.export_deck(result)
            e.page.update()
            e.page.go("/home")            

    def export_deck(self, path):
        with open(path, "wb") as f:
            p.dump(self.deck, f)

    def import_deck(self, files, e):
        self.selected_deck_path = files[0].path
        with open(self.selected_deck_path, "rb") as f:
            self.deck = p.load(f)
        self.card_list.controls.clear()
        self.selected_card_index = -1
        for c in self.deck.cards:
            self.card_list.controls.append(ft.Button(content=ft.Row([ft.Text(c.question), ft.Text(c.answer)], alignment="spaceBetween"), on_click=self.card_selected))
        e.page.update()

    def delete_card(self, e):
        self.deck.cards.pop(self.selected_card_index)
        self.card_list.controls.pop(self.selected_card_index)
        self.selected_card_index = -1
        self.del_card_btn.visible = False
        e.page.update()

    def on_close_empty_dlg(self, e):
        self.empty_dlg.open = False
        e.page.update()
        return True

    def add_card(self, e):
        if self.question_field.value.strip()=="" or self.answer_field.value.strip()=="":
            add_to_overlay(e.page, self.empty_dlg)
            e.page.dialog = self.empty_dlg
            self.empty_dlg.open = True
            e.page.update()
            return

        card = Card(self.question_field.value, self.answer_field.value)
        
        if self.selected_card_index == -1:
            self.deck.cards.append(card)
            self.add_card_button.content = "Add Card"

        else:
            self.deck.cards[self.selected_card_index] = card
            self.add_card_button.content = "Add Card"
            self.selected_card_index = -1
        self.del_card_btn.visible = False
        
        self.question_field.value = ""
        self.answer_field.value = ""

        self.card_list.controls.clear()
        for c in self.deck.cards:
            self.card_list.controls.append(ft.Button(content=ft.Row([ft.Text(c.question), ft.Text(c.answer)], alignment="spaceBetween"), on_click=self.card_selected))
        e.page.update()

    def card_selected(self, e):
        j=0
        for i in self.card_list.controls:
            if i == e.control:
                e.control.bgcolor = ft.Colors.BLUE_200
                self.question_field.value = e.control.content.controls[0].value
                self.answer_field.value = e.control.content.controls[1].value
                self.selected_card_index = j
                self.add_card_button.content = "Update Card"
                self.del_card_btn.visible = True
            else:
                i.bgcolor = None
            j+=1
            
        e.page.update()

    def build(self, e):
        self.select_deck_dlg = ft.FilePicker()
        e.page.update()

        add_to_overlay(e.page, self.init_dialog)
        e.page.dialog = self.init_dialog
        self.init_dialog.open=True
        e.page.update()

        return ft.View(route="/creator", controls=[
            ft.Column([
                self.card_list,
                self.question_field,
                self.answer_field,
                self.add_card_button,
                self.save_deck,
                self.del_card_btn
            ])
        ])