import csv
import os
import sys
import types
import unittest

# Stub consolemenu module required by utils
consolemenu = types.ModuleType("consolemenu")
consolemenu.ConsoleMenu = type("ConsoleMenu", (), {})
items = types.ModuleType("consolemenu.items")
items.FunctionItem = type("FunctionItem", (), {})
sys.modules.setdefault('consolemenu', consolemenu)
sys.modules.setdefault('consolemenu.items', items)

# Ensure project root is on the path when tests are run from the tests directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from flashCards import FlashCardDeck

class FlashCardDeckTestCase(unittest.TestCase):
    def test_kana_test_deck_length(self):
        deck = FlashCardDeck('kana-test.csv')
        with open('kana-test.csv', newline='') as f:
            row_count = sum(1 for _ in csv.reader(f)) - 1  # minus header
        self.assertEqual(len(deck), row_count)

if __name__ == '__main__':
    unittest.main()
