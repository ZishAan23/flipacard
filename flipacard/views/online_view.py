import flet as ft
from src.templates import *
import mysql.connector
import pickle as p

class online_view():
    def __init__(self):
        self.text = ft.Text("Download online flashcard decks from here")
        self.deck_list_ui = ft.ListView()
        self.deck_list = []
        self.selected_deck_index = None
        self.download_btn = ft.TextButton("Download", on_click=self.on_download_click)
        self.back_btn = ft.TextButton("Back", on_click=self.on_back)
        
        self.con, self.c = connect_to_db()
    
    def init_list(self,e):
        self.deck_list_ui.controls = []
        self.download_btn.visible = False
        self.c.execute("SELECT dname,did FROM decks")
        dat = self.c.fetchall()

        for i in dat:
            self.deck_list.append(i[1])
            self.deck_list_ui.controls.append(ft.Container(content=ft.TextButton(i[0], on_click=self.on_deck_click)))
        e.page.update()

    def on_deck_click(self,e):
        j=0
        for i in self.deck_list_ui.controls:
            if i==e.control.parent:
                self.selected_deck_index=j
                i.bgcolor = ft.Colors.BLUE_200
                self.download_btn.visible = True
                break
            else:
                i.bgcolor = None
            j+=1
        else:
            self.selected_deck_index = None
            self.download_btn.visible = False

    def on_download_click(self, e):
        print(self.selected_deck_index)
        if self.selected_deck_index != None:
            did = self.deck_list[self.selected_deck_index]
            self.c.execute("SELECT * FROM decks WHERE did=%s", (did,))
            dat = self.c.fetchone()
            dname = dat[3]
            blob = dat[-1]

                
            from pathlib import Path

            BASE_DIR = Path(__file__).resolve().parent.parent
            DECK_DIR = BASE_DIR / "decks"
            DECK_DIR.mkdir(exist_ok=True)

            pth = DECK_DIR / f"{dname}.fc"

            counter = 1
            while pth.exists():
                pth = DECK_DIR / f"{dname}_{counter}.fc"
                counter += 1


            with open(pth, "wb") as f:
                f.write(blob)

    def on_back(self,e):
        self.con.close()
        e.page.go("/home")
        e.page.update()

    def build(self, e):
        self.con, self.c = connect_to_db()
        self.init_list(e)

        return ft.View(route="/browse",controls=[self.text, self.deck_list_ui, self.download_btn, self.back_btn])

    


