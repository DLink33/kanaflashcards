#!env/Scripts/python

'''
To run from inside the virtual environment:
    $ source env/Scripts/activate
To deactivate the virtual environment:
    $ deactivate
'''

from flashCards import FlashCardDeck

KANA_CSV = "kana.csv"
JAP_VOCAB_CSV = "jap-vocab.csv"

def main():
    flashCardDeck = FlashCardDeck(KANA_CSV)
    cards = flashCardDeck.cards
    for card in cards:
        card.printCard('romaji')
        card.printCard('hiragana')
        card.printCard('katakana')

if __name__ == "__main__":
    main()
