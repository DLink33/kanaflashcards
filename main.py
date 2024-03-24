#!/mingw64/bin/python3

from flashCards import FlashCardDeck
from utils import createMenu as menu
from games import guessCards, customGuessCards
import time

KANA_CSV = "kana.csv"
KANA_TEST_CSV = "kana-test.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"


def main():
    # kanaCardDeck = FlashCardDeck(KANA_CSV)
    kanaCardDeck = FlashCardDeck(KANA_CSV)
    vocabCardDeck = FlashCardDeck(JAP_VOCAB_CSV)
    
    kanaMenuFunctions = {
        "Hiragana to Romaji": {"function": guessCards, "args": [kanaCardDeck, "hiragana", "romaji"]},
        "Katakana to Romaji": {"function": guessCards, "args": [kanaCardDeck, "katakana", "romaji"]},
        "Katakana to Hiragana": {"function": guessCards, "args": [kanaCardDeck, "katakana", "hiragana"]},
        "Hiragana to Katakana": {"function": guessCards, "args": [kanaCardDeck, "hiragana", "katakana"]},
    }
    
    vocabOptions = {
        "all":{"function": guessCards,"args":[vocabCardDeck, "japanese","english"]},
        "by category":{"function": customGuessCards,"args":[vocabCardDeck, "japanese","english"]},
    }
    
    vocabFunctions = {
        "Vocab":{"function":menu ,"args":["Vocab", "", vocabOptions]},
        "Japanese Vocabulary": {"function": guessCards, "args": [vocabCardDeck, "japanese", "english"]},
        "Japanese Pronunciation": {"function": guessCards, "args": [vocabCardDeck, "japanese", "pronunciation"]}
    }
    
    mainMenuFunctions = {
        "Kana":{"function":menu, "args":["Kana Flashcards",  "Hiragana & Katakana", kanaMenuFunctions]},
        "Vocabulary":{"function":menu,"args":["Vocabulary Flashcards", "Japanese Words", vocabFunctions]}
    }

    menu("English ⇆ Japanese", "FlashCards for learning Japanese...", mainMenuFunctions)


if __name__ == "__main__":
    main()
