import mysql.connector as m


class Card:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class Deck:
    def __init__(self, name : str, cards:list[Card]):
        self.name = name
        self.cards = cards
    
    def get_card_at(self, index):
        return self.cards[index]
    
    def move_card_at_end(self, index):
        self.cards.append(self.cards.pop(index))
    
def add_to_overlay(page, dialog):
    if dialog not in page.overlay:
        page.overlay.append(dialog)
        page.update()


from pathlib import Path
def find_deck_files_in(directory_path, ext="fc"):
    # rglob stands for "recursive glob"
    return [str(file) for file in Path(directory_path).rglob(f"*.{ext}")]

from pathlib import Path

def file_exists(path):
    return Path(path).is_file()

def init_db():
    connector, c = connect_to_db() 
    
    c.execute("desc decks")
    print(c.fetchall())
    c.execute("desc users")
    print(c.fetchall())

    #c.execute("""CREATE TABLE decks(
    #            uid INT REFERENCES users(uid),
     #           did INT PRIMARY KEY,
      #          uname VARCHAR(30),
       #         dname VARCHAR(30),
        #        deck BLOB
         #     )""")
    #c.execute("alter table decks modify did INT AUTO_INCREMENT")
    #c.execute("alter table decks modify deck MEDIUMBLOB")
    


    connector.commit()

    connector.close()

def connect_to_db():
    connector = m.connect(host="mysql-2b2177a2-talibzishan-d4d9.h.aivencloud.com", port=28345 , user="avnadmin", passwd="AVNS_H8jJ3kFsaCTS4EGF4SZ", ssl_ca = "ca.pem", connection_timeout=5)

    c = connector.cursor()

    c.execute("USE flipacard")

    return connector,c
