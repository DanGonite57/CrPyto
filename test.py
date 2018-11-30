import operator

import matplotlib.pyplot as plt

lettprobs = {'e': 0.127, 't': 0.0905, 'a': 0.0817, 'o': 0.075, 'i': 0.0697, 'n': 0.0675, 's': 0.0633, 'h': 0.0609, 'r': 0.06, 'd': 0.0425, 'l': 0.0403, 'c': 0.0278, 'u': 0.0276, 'm': 0.0241, 'w': 0.0236, 'f': 0.0223, 'g': 0.0202, 'y': 0.0197, 'p': 0.0193, 'b': 0.015, 'v': 0.0098, 'k': 0.0077, 'j': 0.0015, 'x': 0.0015, 'q': 0.0095, 'z': 0.0074}

fig, ax = plt.subplots(figsize=(10, 5))

probs = [lettprobs.get(x, 0) for x in sorted(lettprobs)]
barwidth = 0.3

ax.bar([x for x in map(operator.sub, range(len(lettprobs)), [barwidth / 2] * len(probs))], probs, width=barwidth)
ax.bar([x for x in map(operator.add, range(len(lettprobs)), [barwidth / 2] * len(probs))], probs, width=barwidth)
ax.set_xticks(range(len(lettprobs)))
ax.set_xticklabels(map(str.upper, sorted(lettprobs)))

plt.show()
