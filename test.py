import operator
from string import ascii_lowercase as ALPH

import matplotlib.pyplot as plt

from Formatting import SpaceRem
from Processing import FreqAnalysis

ciph = ""

lettprobs = {'e': 0.127, 't': 0.0905, 'a': 0.0817, 'o': 0.075, 'i': 0.0697, 'n': 0.0675, 's': 0.0633, 'h': 0.0609, 'r': 0.06, 'd': 0.0425, 'l': 0.0403, 'c': 0.0278, 'u': 0.0276, 'm': 0.0241, 'w': 0.0236, 'f': 0.0223, 'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.015, 'v': 0.0098, 'k': 0.0077, 'j': 0.0015, 'x': 0.0015, 'q': 0.0095, 'z': 0.0074}

fig, ax = plt.subplots(figsize=(10, 5))

lettcounts = [lettprobs.get(x, 0) for x in sorted(ALPH)]
print(lettcounts)
barwidth = 0.3

ciphprobs = FreqAnalysis.getFrequencies(ciph)
ax.bar([x for x in map(operator.sub, range(len(lettprobs)), [barwidth / 2] * len(lettcounts))], lettcounts, width=barwidth, label="English", color="r")
try:
    ciphcounts = [ciphprobs.get(x, 0) / len(ciph) for x in sorted(ALPH)]
    ax.bar([x for x in map(operator.add, range(len(ciphprobs)), [barwidth / 2] * len(ciphcounts))], ciphcounts, width=barwidth, label="Cipher Text", color="b")
except ZeroDivisionError:
    pass
ax.get_yaxis().set_visible(False)
ax.set_xticks(range(len(lettprobs)))
ax.set_xticklabels(map(str.upper, sorted(lettprobs)))
ax.legend()

plt.show()
