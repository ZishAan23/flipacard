import flet as ft
from src.templates import *
import pickle as p

class practice_view():
    def __init__(self, deck):
        self.deck = deck
        self.current_card_index = 0
        self.show_answer_btn = ft.TextButton("Show Answer", on_click=self.show_answer)
        self.question = ft.Text(self.deck.get_card_at(self.current_card_index).question)
        self.answer = ft.Text("Answer: " + self.deck.get_card_at(self.current_card_index).answer)
        self.check_dlg = ft.AlertDialog(title=ft.Text("Check"), content=ft.Column([ft.Text("Is this correct?"), self.answer]), actions=[
            ft.TextButton("Yes", on_click=self.correct),
            ft.TextButton("No", on_click=self.incorrect)
        ])
        self.upload_btn = ft.TextButton("Upload Deck", on_click=self.on_upload)
        self.upload_name_field = ft.TextField()
        self.upload_dlg = ft.AlertDialog(content=self.upload_name_field, actions=[ft.TextButton("upload", on_click=self.upload_final)])
        self.back_btn = ft.TextButton("back", on_click=self.on_back_btn)

    def show_answer(self, e):
        add_to_overlay(e.page, self.check_dlg)
        self.check_dlg.open = True
        e.page.update()
    
    def correct(self, e):
        if len(self.deck.cards) <= self.current_card_index + 1:
            e.page.go("/home")
            return
        self.current_card_index += 1
        self.check_dlg.open = False
        e.page.dialog = None
        self.question.value = self.deck.get_card_at(self.current_card_index).question
        self.answer.value = self.deck.get_card_at(self.current_card_index).answer
        e.page.update()
    
    def incorrect(self, e):
        self.check_dlg.open = False
        e.page.dialog = None
        self.deck.move_card_at_end(self.current_card_index)
        self.question.value = self.deck.get_card_at(self.current_card_index).question
        self.answer.value = self.deck.get_card_at(self.current_card_index).answer
        e.page.update()

    def on_upload(self,e):
        add_to_overlay(e.page, self.upload_dlg)
        self.upload_dlg.open = True
        e.page.dialog = self.upload_dlg
        e.page.update()

    def upload_final(self,e):
        con,c = connect_to_db()
        data = p.dumps(self.deck)

        uid = e.page.session.store.get("uid")
        uname = e.page.session.store.get("uname")
        dname = self.upload_name_field.value
        
        ins = "INSERT INTO decks(uid, uname, dname, deck) values(%s,%s,%s,%s)"

        c.execute(ins, (uid, uname , dname, data))

        con.commit()
        con.close()
        self.upload_dlg.open= False
        e.page.dialog = None
        e.page.update()
    
    def on_back_btn(self,e):
        e.page.go("/home")
        e.page.update()

    
    def build(self, e):
        return ft.View(route="/practice", controls=[ft.Text("Practice"), self.question, self.show_answer_btn, self.upload_btn, self.back_btn])
