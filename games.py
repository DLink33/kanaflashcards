import flashCards


def guessCards(flashCardDeck, ):
    deck = flashCardDeck
    flashCardDeck.shuffle()


def printCards(flashCardDeck):
    cards = flashCardDeck.cards
    for card in cards:
        card.printCard(list(card.sides.keys())[0])
