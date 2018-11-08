import collections


def getFrequencies(text):
    return collections.Counter(text).most_common()
