#!/mingw64/bin/python3

from flashCards import FlashCardDeck
from utils import createMenu as menu
from games import printCards, guessCards
import time

KANA_CSV = "kana.csv"
KANA_TEST_CSV = "kana-test.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"


def main():
    # kanaCardDeck = FlashCardDeck(KANA_CSV)
    kanaCardDeck = FlashCardDeck(KANA_CSV)
    vocabCardDeck = FlashCardDeck(JAP_VOCAB_CSV)
    functions = {
        "Hiragana to Romaji": {"function": guessCards, "args": [kanaCardDeck, "hiragana", "romaji"]},
        "Katakana to Romaji": {"function": guessCards, "args": [kanaCardDeck, "katakana", "romaji"]},
        "Katakana to Hiragana": {"function": guessCards, "args": [kanaCardDeck, "katakana", "hiragana"]},
        "Japanese Vocabulary": {"function": guessCards, "args": [vocabCardDeck, "japanese", "english"]},
        "Japanese Pronunciation": {"function": guessCards, "args": [vocabCardDeck, "japanese", "pronunciation"]}
    }

    menu("English ⇆ Japanese", "FlashCards for learning Japanese...", functions)


if __name__ == "__main__":
    main()
