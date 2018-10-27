import itertools
import math


def decrypt(ciph):
    length = len(ciph)
    for i in range(3, length):
        temp = str(ciph)
        rows = []
        text = [""] * i
        while True:
            rows.append([x for x in temp[:i]])
            temp = temp.replace(temp[:i], "", 1)
            if temp == "":
                break
        for j in range(i):
            for k in range(len(rows)):
                try:
                    text[j] += rows[k][j]
                except IndexError:
                    break

        poss = [[]] * math.factorial(i)
        for j, k in enumerate(itertools.permutations(range(len(text)))):
            poss[j] = [text[k[x]] for x in range(len(text))]

        newText = ""
        for cols in poss:
            print(cols)
            for j in range(i):
                print(j)
                for k in range(len(cols[j])):
                    print(cols[j][k])
                    try:
                        newText += cols[j][k]
                    except IndexError:
                        break
            print(newText)
            return "", 0
