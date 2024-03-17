#!/mingw64/bin/python3

from flashCards import FlashCardDeck
from utils import createMenu as menu
from games import printCards
import time

KANA_CSV = "kana.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"


def func1():
    print("This is function 1")
    time.sleep(2)


def func2():
    print("This is function 2")
    time.sleep(2)


def func3():
    print("This is function 3")
    time.sleep(2)


def main():
    flashCardDeck = FlashCardDeck(KANA_CSV)
    vocabCardDeck = FlashCardDeck(JAP_VOCAB_CSV)
    kanaCards = flashCardDeck.cards
    vocabCards = vocabCardDeck.cards
    kanaCards[0].printCard('hiragana')
    kanaCards[0].printCard('romaji')
    kanaCards[0].printCard('katakana')
    print()
    vocabCards[0].printCard('english')
    vocabCards[0].printCard('japanese')

    functions = {
        "Print Cards": {"function": printCards, "args": [flashCardDeck]},
        "Func2": {"function": func2, "args": []},
        "Func3": {"function": func3, "args": []}
    }

    menu("English ⇆ Japanese", "FlashCards for learning Japanese...", functions)


if __name__ == "__main__":
    main()
