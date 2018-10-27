from Ciphers import *
from Formatting import PuncRem


def decrypt(ciph, cipher):
    ciph = PuncRem.remove(ciph)
    result, score = eval(cipher.capitalize()).decrypt(ciph)
    return result, score
