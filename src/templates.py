
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


