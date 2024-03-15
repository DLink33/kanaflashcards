import csv
import random
from unicodedata import east_asian_width as eWidth

class FlashCard:
    def __init__(self, sides):
        self.sides = sides

    def __str__(self):
        string = ""
        for value in self.sides.values():
            string+=','+str(value)
        return string[1:]

    def check(self, guess, side):
        return guess == side.value()

class KanaFlashCard(FlashCard):
    def __init__(self, romaji, hiragana, katakana):
        super().__init__({'romaji':romaji, 'hiragana':hiragana, 'katakana':katakana})

    def printCard(self, kanaType):
        value = self.sides.get(kanaType, "")
        length = len(value)
        padding = 2
        if length == 1:
            width = 2 if eWidth(value) in ('F', 'W') else 1
            middle_line = "│" + " " * padding + value + " " * (padding-1) + "│"
        else:
            width = length
            middle_line = "│" + " " * padding + value + " " * padding + "│"
        top_border = "┌" + "─" * (width + 2*padding) + "┐"
        mid1 = "│"+ " " * (width + 2*padding) + "│"
        mid2 = "│"+ " " * (width + 2*padding) + "│"
        bottom_border = "└" + "─" * (width + 2*padding) + "┘"
        print(top_border)
        print(mid1)
        print(middle_line)
        print(mid2)
        print(bottom_border)


class FlashCardDeck:
    def __init__(self, csvFile):
        self.cards = []
        self.generateCards(csvFile)

    def __str__(self):
        return f"{self.cards}"
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, index):
        return self.cards[index]
    def generateCards(self, csvFile):
        with open(csvFile, 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            numColumns = len(next(reader))
            if numColumns == 2:
                for row in reader:
                    self.cards.append(FlashCard(row[0], row[1]))
            elif numColumns == 3:
                for row in reader:
                    self.cards.append(KanaFlashCard(row[0], row[1], row[2]))
            else:
                print("Invalid number of columns in csv file")
    def shuffle(self):
        random.shuffle(self.cards)
