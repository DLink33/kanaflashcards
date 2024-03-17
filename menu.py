from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem


def createMenu(title, subtitle, functions):

    # Create the menu
    menu = ConsoleMenu(str(title), str(subtitle))

    # Create some items
    for name, function in functions.items():
        item = FunctionItem(name, function)
        menu.append_item(item)

    # Show the menu
    menu.show()
