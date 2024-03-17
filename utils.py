from unicodedata import east_asian_width as eaw
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem


def createMenu(title, subtitle, functions):

    # Create the menu
    menu = ConsoleMenu(str(title), str(subtitle))

    # Create some items
    for name, function_info in functions.items():
        item = FunctionItem(
            name, function_info["function"], function_info["args"])
        menu.append_item(item)

    # Show the menu
    menu.show()


def calcStrWidth(string):
    width = 0
    for c in string:
        if eaw(c) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width
