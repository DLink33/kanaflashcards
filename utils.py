from unicodedata import east_asian_width as eaw


def calcStrWidth(string):
    width = 0
    for c in string:
        if eaw(c) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width
