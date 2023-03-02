from card import Card
from subprocess import call
import os

def create_all_cards():
    deck = []
    for color in ["red", "green", "blue", "yellow"]:
        for number in range(1, 10):
            deck.append(Card(color, number, None))
        for special_ability in ["reverse", "skip"]: # , "reverse", "+2", "wild", "wild+4"
            deck.append(Card(color, special_ability=special_ability))

    # deck.append(Card(special_ability="+4"))
    # deck.append(Card(special_ability="+4"))
    # deck.append(Card(special_ability="everything"))
    # deck.append(Card(special_ability="everything"))

    return deck

def clear():
    _ = call('clear' if os.name =='posix' else 'cls')