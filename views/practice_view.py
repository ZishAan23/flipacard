import flet as ft
from src.templates import *

class practice_view():
    def __init__(self, deck):
        self.deck = deck
        self.current_card_index = 0
        self.show_answer_btn = ft.TextButton("Show Answer", on_click=self.show_answer)
        self.question = ft.Text(self.deck.get_card_at(self.current_card_index).question)
        self.check_dlg = ft.AlertDialog(title=ft.Text("Check"), content=ft.Column([ft.Text("Is this correct?"), ft.Text("Answer: " + self.deck.get_card_at(self.current_card_index).answer)]), actions=[
            ft.TextButton("Yes", on_click=self.correct),
            ft.TextButton("No", on_click=self.incorrect)
        ])

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
        e.page.update()
    
    def incorrect(self, e):
        self.check_dlg.open = False
        e.page.dialog = None
        self.deck.move_card_at_end(self.current_card_index)
        self.question.value = self.deck.get_card_at(self.current_card_index).question
        e.page.update()
    
    def build(self, e):
        return ft.View(route="/practice", controls=[ft.Text("Practice"), self.question, self.show_answer_btn])