#!/mingw64/bin/python3

import argparse
import os

from db import MySQLFlashcardRepository
from flashCards import FlashCardDeck
from gui import run_gui

KANA_DECK = "kana"
JAP_VOCAB_DECK = "jap-vocab"


def clearTerm():
    os.system("cls" if os.name == "nt" else "clear")


def kanaPracticeMenu(kanaCardDeck, kanas):
    from games import customGuessCards, guessCards
    from utils import createMenu as menu
    from utils import getUserInput

    shownKana = getUserInput(
        "Enter what kana type you want shown:\n  - Romaji\n  - Hiragana\n  - Katakana\n",
        ["r", "h", "k"],
    )[0].lower()
    clearTerm()
    guessKana = getUserInput(
        "Enter what kana type you want to guess:\n  - Romaji\n  - Hiragana\n  - Katakana\n",
        ["r", "h", "k"],
    )[0].lower()
    key = {"k": "katakana", "r": "romaji", "h": "hiragana"}

    kanaMenuFunctions = {
        "All": {
            "function": guessCards,
            "args": [kanaCardDeck, key[shownKana], key[guessKana]],
        },
        "Custom": {
            "function": customGuessCards,
            "args": [kanaCardDeck, kanas, key[shownKana], key[guessKana]],
        },
    }

    menu(
        f"{key[shownKana].capitalize()} ⟶   {key[guessKana].capitalize()}",
        "",
        kanaMenuFunctions,
    )


def vocabPracticeMenu(vocabCardDeck, vocabTags):
    from games import customGuessCards, guessCards
    from utils import createMenu as menu
    from utils import getUserInput

    shownSide = getUserInput(
        "Enter what you want shown:\n  - English\n  - Romaji\n  - Kana (no Kanji)\n  - Kana (with Kanji)\n",
        ["english", "romaji", "kana", "kanji"],
    ).lower()
    clearTerm()
    guessSide = getUserInput(
        "Enter what kana type you want to guess:\n  - English\n  - Romaji\n  - Kana (no Kanji)\n  - Kana (with Kanji)\n",
        ["english", "romaji", "kana", "kanji"],
    ).lower()

    vocabMenuFunctions = {
        "All": {"function": guessCards, "args": [vocabCardDeck, shownSide, guessSide]},
        "Custom": {
            "function": customGuessCards,
            "args": [vocabCardDeck, vocabTags, shownSide, guessSide],
        },
    }

    menu(
        f"{shownSide.capitalize()} ⟶   {guessSide.capitalize()}", "", vocabMenuFunctions
    )


def main():
    from games import customGuessCards, guessCards
    from utils import createMenu as menu

    repository = MySQLFlashcardRepository()
    kanaCardDeck = FlashCardDeck(deck_name=KANA_DECK, repository=repository)
    vocabCardDeck = FlashCardDeck(deck_name=JAP_VOCAB_DECK, repository=repository)
    vocabTags = []
    kanaTags = []
    for card in vocabCardDeck.cards:
        for tag in card.sides["tags"][1:-1].split(" "):
            if tag not in vocabTags:
                vocabTags.append(tag)
    for card in kanaCardDeck.cards:
        for tag in card.sides["tags"][1:-1].split(" "):
            if tag not in kanaTags:
                kanaTags.append(tag)
    vocabTags.sort()
    kanaTags.sort()

    vocabMenuFunctions = {
        "All": {"function": guessCards, "args": [vocabCardDeck, "kana", "english"]},
        "By Category": {
            "function": customGuessCards,
            "args": [vocabCardDeck, vocabTags, "kana", "english"],
        },
    }

    vocabFunctions = {
        "Vocabulary": {
            "function": menu,
            "args": ["Japanese (日本語) Vocabulary", "", vocabMenuFunctions],
        },
        "Pronunciation": {
            "function": guessCards,
            "args": [vocabCardDeck, "kana", "romaji"],
        },
    }

    mainMenuFunctions = {
        "Kana": {"function": kanaPracticeMenu, "args": [kanaCardDeck, kanaTags]},
        "Vocabulary (Beta)": {
            "function": vocabPracticeMenu,
            "args": [vocabCardDeck, vocabTags],
        },
        "Vocabulary": {
            "function": menu,
            "args": ["Vocabulary Flashcards", "Japanese Words", vocabFunctions],
        },
    }

    menu("English ⇆ Japanese", "FlashCards for learning Japanese...", mainMenuFunctions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Japanese flashcards")
    parser.add_argument("--gui", action="store_true", help="Launch the desktop GUI")
    args = parser.parse_args()

    if args.gui:
        run_gui()
    else:
        main()
