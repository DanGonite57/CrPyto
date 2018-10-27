import string

with open("rawWords.txt") as f:
    words = f.read()

print(0)
words = words.split()
print(1)
f = open("WordList.txt", "a")
print(2)

tmp = set()
print(3)
for word in words:
    if word.isalnum():
        tmp.add(word.lower())
print(4)
tmp = sorted(tmp)
print(5)
for x in tmp:
    f.write(x+"\n")
f.close()


#import PatternGen
#
#patterns = {}
#
#with open("D:\Programming\RandPy\Codebreaking No. 3\Ciphers\WordList.txt") as f:
#    words = f.readlines()
#
#for word in words:
#    word = word[:-1]
#    try:
#        patterns[PatternGen.pattern(word)].append(word)
#    except KeyError:
#        patterns[PatternGen.pattern(word)] = []
#        patterns[PatternGen.pattern(word)].append(word)
#
#f = open("D:\Programming\RandPy\Codebreaking No. 3\Ciphers\PatternList.py", "w")
#f.write(str(patterns))
#f.close()
