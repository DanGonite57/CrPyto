from string import ascii_letters as ALPH


def remove(text, chars):
    for char in chars:
        text = text.replace(char, "")
    return text


def readd(new, old):
    new = [x for x in new]
    for i, char in enumerate(old):
        if char not in ALPH:
            try:
                if new[i] != char:
                    new.insert(i, char)
            except IndexError:
                new.append(char)
    return ''.join(new)
