#!/mingw64/bin/python3

from flashCards import FlashCardDeck
from utils import createMenu as menu
from utils import getUserInput
from games import guessCards, customGuessCards
import os

KANA_CSV = "kana.csv"
KANA_TEST_CSV = "kana-test.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"

def kanaPracticeMenu(kanaCardDeck, kanas):
    shownKana = getUserInput("Enter what kana type you want shown:\n  - Romaji\n  - Hiragana\n  - Katakana\n",['r', 'h', 'k'])[0].lower()
    os.system('cls')
    guessKana = getUserInput("Enter what kana type you want to guess:\n  - Romaji\n  - Hiragana\n  - Katakana\n",['r', 'h', 'k'])[0].lower()
    key = {"k":"katakana","r":"romaji","h":"hiragana"}
    
    kanaMenuFunctions = {
    "All": {"function": guessCards, "args":[kanaCardDeck, key[shownKana], key[guessKana]]},
    "Custom": {"function": customGuessCards, "args":[kanaCardDeck, kanas, key[shownKana], key[guessKana]]},
    }
    
    menu(f"{key[shownKana].capitalize()} ⟶   {key[guessKana].capitalize()}", "", kanaMenuFunctions)

def main():
    # kanaCardDeck = FlashCardDeck(KANA_CSV)
    kanaCardDeck = FlashCardDeck(KANA_CSV)
    vocabCardDeck = FlashCardDeck(JAP_VOCAB_CSV)
    vocabTags = []
    kanaTags = []
    for card in vocabCardDeck.cards:
        for tag in card.sides['tags'][1:-1].split(" "):
            if tag not in vocabTags:
                vocabTags.append(tag)
    for card in kanaCardDeck.cards:
        for tag in card.sides['tags'][1:-1].split(" "):
            if tag not in kanaTags:
                kanaTags.append(tag)
    vocabTags.sort()
    kanaTags.sort()

    vocabMenuFunctions = {
        "All": {"function": guessCards, "args": [vocabCardDeck, "japanese", "english"]},
        "By Category": {"function": customGuessCards, "args": [vocabCardDeck, vocabTags, "japanese", "english"]},
    }

    vocabFunctions = {
        "Vocabulary": {"function": menu, "args": ["Japanese (日本語) Vocabulary", "", vocabMenuFunctions]},
        "Pronunciation": {"function": guessCards, "args": [vocabCardDeck, "japanese", "pronunciation"]}
    }

    mainMenuFunctions = {
        "Kana": {"function": kanaPracticeMenu, "args": [kanaCardDeck, kanaTags]},
        "Vocabulary": {"function": menu, "args": ["Vocabulary Flashcards", "Japanese Words", vocabFunctions]}
    }

    menu("English ⇆ Japanese", "FlashCards for learning Japanese...", mainMenuFunctions)

if __name__ == "__main__":
    main()
