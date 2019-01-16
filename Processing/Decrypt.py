# NOW DEPRECATED #

from string import puntuation as PUNC

import Ciphers
from Formatting import Format


def decrypt(ciph, cipher):
    ciph = Format.remove(ciph, PUNC)
    result, score = eval("Ciphers." + cipher.capitalize()).decrypt(ciph)
    return result, score
