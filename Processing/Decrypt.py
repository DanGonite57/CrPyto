import Ciphers
from Formatting import PuncRem


def decrypt(ciph, cipher):
    ciph = PuncRem.remove(ciph)
    result, score = eval("Ciphers." + cipher.capitalize()).decrypt(ciph)
    return result, score
