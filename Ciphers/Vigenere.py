import collections
import itertools
import string

from Processing import DetectEnglish


def decrypt(ciph):
    ciph = ciph.lower()

    # Find repeats
    sub = {}
    for i in range(3, len(ciph)):
        for j in range(len(ciph) - i):
            try:
                sub[ciph[j: j + i]].append(j)
            except KeyError:
                sub[ciph[j: j + i]] = [j]

    # Remove non-dupes
    temp = dict(sub)
    for x in sub:
        if len(sub[x]) == 1:
            temp.pop(x)
    sub = temp

    print(sub)
    # return

    # Get keylens
    keylens = []
    for x in sub:
        for i in range(len(sub[x]) - 1):
            keylens.append(sub[x][i + 1] - sub[x][i])

    # Get keylen factors
    factors = []
    for i in keylens:
        factors += [j for j in range(2, i + 1) if i % j == 0]

    factors = [x[0] for x in collections.Counter(factors).most_common() if x[1] == collections.Counter(factors).most_common(1)[0][1]]
    print(factors)

    # Get substrings
    # TODO: Use this block in transposition columnising
    best = ""
    bestScore = 0
    for i in factors:  # TODO: Change back to factors
        substrings = []
        keycombos = []
        posssubs = {}
        for j in range(i):
            substring = ''.join([ciph[x] for x in range(j, len(ciph), i)])
            substrings.append(substring)
            print(substring)

            a = b = string.ascii_lowercase
            posssubs[j] = {}
            poss = []
            for k in range(26):
                new = ""
                for l in substring:
                    new += (b[a.index(l)])
                print(new, DetectEnglish.freqMatch((''.join(new)))) # TODO: Switch back to freqMatch IC no work
                # return
                poss.append((a[k], DetectEnglish.freqMatch(''.join(new))))
                b = b[-1] + b[:-1]
                posssubs[j][a[k]] = new


            bestFreq = 1
            keys = []
            print(poss)
            for x in poss:
                if x[1] > bestFreq:
                    bestFreq = x[1]
                    keys = []
                    keys.append(x[0])
                elif x[1] == bestFreq:
                    keys.append(x[0])
            keycombos.append(keys)

        print(posssubs)
        
        print(keycombos)
        
        combos = []
        comboGen(keycombos, combos, 0, [[]] * len(keycombos))
        print(combos)

        results = []

        for combo in combos:
            result = [[]] * len(ciph)
            for j, x in enumerate(combo):
                result[j::i] = posssubs[j][x]
            results.append(''.join(result))
        
        for result in results:
            score = DetectEnglish.detect(result)
            if score > bestScore:
                bestScore = score
                best = result
    return result, score

    # return result, score


def comboGen(groups, combos, i, result):
    try:
        for letter in groups[i]:
            result[i] = letter
            comboGen(groups, combos, i + 1, result)
    except IndexError:
        combos.append(''.join(result))
        return
