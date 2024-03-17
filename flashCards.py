import csv
import random
from utils import calcStrWidth


class FlashCard:
    def __init__(self, index, **sides):
        self.sides = sides
        self.index = index

    def __str__(self):
        string = ""
        for value in self.sides.values():
            string += ','+str(value)
        return string[1:]

    def check(self, guess, side):
        return guess == self.sides[side]

    def printCard(self, side):
        value = self.sides[side]
        width = calcStrWidth(value)
        padding = 2
        top_border = "┌" + "─" * (width + 2*padding) + "┐"
        mid1 = "│" + " " * (width + 2*padding) + "│"
        middle_line = "│" + " " * padding + value + " " * padding + "│"
        mid2 = "│" + " " * (width + 2*padding) + "│"
        bottom_border = "└" + "─" * (width + 2*padding) + "┘"
        print(top_border)
        print(mid1)
        print(middle_line)
        print(mid2)
        print(bottom_border)


class KanaFlashCard(FlashCard):
    def __init__(self, romaji, hiragana, katakana, index):
        super().__init__(index, r=romaji, h=hiragana, k=katakana)


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

    def generateCards(self, csvFile, encoding='UTF-8'):
        with open(csvFile, 'r', encoding=encoding) as file:
            reader = csv.reader(file)
            headers = next(reader)
            for i, row in enumerate(reader):
                sides = {header.lower(): value for header,
                         value in zip(headers, row)}
                self.cards.append(FlashCard(i, **sides))

    def shuffle(self):
        random.shuffle(self.cards)
