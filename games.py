import flashCards
import msvcrt
import os


def guessCard(card, sideKey, ansKey):
    os.system('cls' if os.name == 'nt' else 'clear')
    card.printCard(sideKey)
    userIn = input(f"Enter the {ansKey} for this card: ")
    if not card.check(userIn, ansKey):
        print("Incorrect. Nice try!")
        input("Press Enter to continue")
        return False
    else:
        print("Correct!")
        input("Press Enter to continue")
        return True


def handleMissedCards(missedCards, sideKey, ansKey):
    while len(missedCards) > 0:
        userIn = input(
            "Would you like to practice the card you missed? (Y/N): ").lower()
        while userIn not in ["y", "n"]:
            userIn = input("Invalid input. Please enter Yes or No:").lower()
        if userIn == "y":
            for i in range(len(missedCards)):
                card = missedCards.pop()
                if not guessCard(card, sideKey, ansKey):
                    missedCards.insert(0, card)
        else:
            break


def guessCards(flashCardDeck, sideKey, ansKey):
    deck = flashCardDeck
    deck.shuffle()
    missedCards = []
    sides = deck.cards[0].sides
    keys = sides.keys()
    if sideKey not in keys or ansKey not in keys:
        print("ERROR: Invalid side-type.")
        return
    for card in deck.cards:
        if not guessCard(card, sideKey, ansKey):
            missedCards.append(card)
    print("All cards reviewed.")
    if len(missedCards) == 0:
        input("Press Enter to return to menu")
        return
    handleMissedCards(missedCards, sideKey, ansKey)
    input("Missed cards reviewed! Press Enter to return to menu")


def printCards(flashCardDeck):
    cards = flashCardDeck.cards
    for card in cards:
        card.printCard(list(card.sides.keys())[0])
    userIn = None
    print("Press Enter to return to menu")
    while msvcrt.getch() != b'\r':
        pass
    return
