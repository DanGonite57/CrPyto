def pattern(word):
    contains = []
    result = []
    for letter in word:
        if letter not in contains:
            contains.append(letter)
        result.append(str(contains.index(letter)))
    return ".".join(result)
