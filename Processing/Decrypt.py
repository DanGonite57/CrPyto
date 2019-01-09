import Ciphers
from Formatting import Format


def decrypt(ciph, cipher):
    ciph = Format.remove(ciph)
    result, score = eval("Ciphers." + cipher.capitalize()).decrypt(ciph)
    return result, score
