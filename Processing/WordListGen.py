import PatternGen

with open("rawWords.txt") as f:
    words = f.read()

words = words.split()
f = open("WordList.txt", "a")

tmp = set()
for word in words:
    if word.isalnum() and len(word) > 1:
        tmp.add(word.lower())
tmp = sorted(tmp)
for x in tmp:
    f.write(x + "\n")
f.close()

patterns = {}

with open("WordList.txt") as f:
    words = f.readlines()

for word in words:
    word = word[:-1]
    try:
        patterns[PatternGen.pattern(word)].append(word)
    except KeyError:
        patterns[PatternGen.pattern(word)] = []
        patterns[PatternGen.pattern(word)].append(word)

f = open("PatternList.py", "w")
f.write(str(patterns))
f.close()
