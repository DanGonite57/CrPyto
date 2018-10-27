from string import ascii_lowercase, digits, whitespace


def remove(text):
    return ''.join(char for char in text.lower() if char in ascii_lowercase + digits + whitespace)
