import flet as ft 
import views.creator_view as cv
import views.home_view as hv
import views.practice_view as pv
import views.auth_view as av
import views.online_view as ov
from src.templates import *


init_db()

def main(page: ft.Page):
    
    page.title = "Flashcards app"
    page.alignment = ft.MainAxisAlignment.CENTER
    page.spacing = 30

    #defining view objects here
    creatorView = cv.creator_view()
    homeView = hv.home_view()
    authView = av.auth_view()
    onlineView = ov.online_view()

    def route_change(e):
        page.views.clear()
        if e.route == "/home":
            page.views.append(
                homeView.build(e)
            )
        elif e.route == "/creator":
            page.views.append(
                creatorView.build(e)
            )
        elif e.route == "/practice":
            selected_deck = page.session.store.get("selected_deck")
            practiceView = pv.practice_view(selected_deck)
            page.views.append(
                practiceView.build(e)
            )
        elif e.route == "/login":
            page.views.append(authView.build_login(e))
        elif e.route == "/signup":
            page.views.append(authView.build_signup(e))
        elif e.route == "/browse":
            page.views.append(onlineView.build(e))
        page.update()

    page.on_route_change = route_change

    page.go("")
    page.go("/home") # no need to call update when not chanignging uis

if __name__ == "__main__":
    ft.app(target=main)


#for hot reload use this command 
#& "C:\Users\Touhid\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\flet.exe" run main.py

