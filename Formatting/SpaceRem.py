from string import whitespace


def remove(text):
    return ''.join(char for char in text if char not in whitespace)
