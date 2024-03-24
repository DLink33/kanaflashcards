import msvcrt
import os


def guessCard(card, sideKey, ansKey):
    os.system('cls' if os.name == 'nt' else 'clear')
    card.printCard(sideKey)
    userIn = input(f"Enter the {ansKey} for this card: ")
    if userIn.lower() == 'exit':
        return 'exit'
    if not card.check(userIn, ansKey):
        print("Incorrect. Nice try!")
        userIn = input("1. Show answer\n2. Continue...\n")
        while userIn != '1' and userIn != '2' and userIn.lower() != 'exit':
            userIn = input()
        if userIn.lower() == 'exit':
            return 'exit'
        if userIn == '1':
            os.system('cls')
            card.printCard(ansKey)
            input("Press Enter to continue\n")
        return False
    else:
        print("Correct!")
        input("Press Enter to continue")
        return True

def handleMissedCards(missedCards, sideKey, ansKey):
    while len(missedCards) > 0:
        userIn = input(
            "Would you like to practice the cards you missed? (Y/N):\n").lower()
        while userIn not in ["y", "n"] and userIn != 'exit':
            userIn = input("Invalid input. Please enter Yes or No:\n").lower()
        if userIn == 'exit':
            return 'exit'
        if userIn == "y":
            for i in range(len(missedCards)):
                card = missedCards.pop()
                result = guessCard(card, sideKey, ansKey)
                if result == 'exit':
                    return 'exit'
                if not result:
                    missedCards.insert(0, card)
        else:
            break

def guessCards(flashCardDeck, sideKey, ansKey):
    totalPoints = 0
    points = 0
    deck = flashCardDeck
    deck.shuffle()
    missedCards = []
    sides = deck.cards[0].sides
    keys = sides.keys()
    if sideKey not in keys or ansKey not in keys:
        print("ERROR: Invalid side-type.")
        return
    for card in deck.cards:
        totalPoints += 1
        result = guessCard(card, sideKey, ansKey)
        if result == 'exit':
            totalPoints -= 1
            if totalPoints != 0:
                score = f"Score: {points}/{totalPoints} or {points/totalPoints*100:.2f}%\n"
            else:
                score = "Score: 0/0 or 0.00%\n"
            print(score)
            input("Press Enter to return to menu\n")
            return
        if not result:
            missedCards.append(card)
        else:
            points += 1
    print("All cards reviewed.\n")
    score = f"Score: {points}/{totalPoints} or {points/totalPoints*100:.2f}%\n"
    print(score)
    if len(missedCards) == 0:
        input("Press Enter to return to menu\n")
        return
    if handleMissedCards(missedCards, sideKey, ansKey) == 'exit':
        return
    input("Missed cards reviewed! Press Enter to return to menu\n")

def customGuessCards(flashCardDeck, sideKey, ansKey):
    cardType = input("Enter the category of cards you would like to review: ")
    totalPoints = 0
    points = 0
    deck = flashCardDeck
    deck.shuffle()
    customDeck = []
    for card in deck.cards:
        if cardType == card.sides['category']:
            print(card.sides['category'])
            customDeck.append(card)
    if customDeck == []:
        print("No cards found in that category.")
        input("Press Enter to return to menu\n")
        return
    missedCards = []
    input("Press Enter to continue")
    for card in customDeck:
        totalPoints += 1
        result = guessCard(card, sideKey, ansKey)
        if result == 'exit':
            totalPoints -= 1
            if totalPoints != 0:
                score = f"Score: {points}/{totalPoints} or {points/totalPoints*100:.2f}%\n"
            else:
                score = "Score: 0/0 or 0.00%\n"
            print(score)
            input("Press Enter to return to menu\n")
            return
        if not result:
            missedCards.append(card)
        else:
            points += 1
    print("All cards reviewed.\n")
    score = f"Score: {points}/{totalPoints} or {points/totalPoints*100:.2f}%\n"
    print(score)
    if len(missedCards) == 0:
        input("Press Enter to return to menu\n")
        return
    if handleMissedCards(missedCards, sideKey, ansKey) == 'exit':
        return
    input("Missed cards reviewed! Press Enter to return to menu\n")

def printCards(flashCardDeck):
    cards = flashCardDeck.cards
    for card in cards:
        card.printCard(list(card.sides.keys())[0])
    userIn = None
    print("Press Enter to return to menu")
    while msvcrt.getch() != b'\r':
        pass
    return
