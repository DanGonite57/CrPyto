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
    return

    # Get substrings
    # TODO: Use this block in transposition columnising
    for i in [factors[1]]:  # TODO: Change back to factors
        substrings = []
        keycombos = []
        for j in range(i):
            substring = ''.join([ciph[x] for x in range(j, len(ciph), 3)])
            substrings.append(substring)
            print(substring)

            a = b = string.ascii_lowercase
            poss = []
            for k in range(26):
                new = ""
                for l in substring:
                    new += (b[a.index(l)])
                poss.append((a[k], DetectEnglish.freqMatch(''.join(new))))
                b = b[1::] + b[0]

            bestFreq = 0
            keys = []
            print(poss)
            for x in poss:
                if x[1] > bestFreq:
                    bestFreq = x[1]
                    keys = []
                    keys.append(x[0])
                elif x[1] == bestFreq:
                    keys.append(x[0])
                print(keys)
            keycombos.append(keys)
        
        combos = []
        comboGen(keycombos, combos, 0, [[]] * len(keycombos))
        print(combos)

        alph = string.ascii_lowercase  # TODO: Move to top and remove b, also for caesar
        # Decrypt using keys
        for combo in combos:
            result = ""
            for i, letter in enumerate(ciph):
                shift = alph.index(combo[i % 3])
                b = alph[shift::] + alph[:shift]
                result += b[a.index(letter)]
                print(shift, b, letter, result)
                return


    # return result, score


def comboGen(groups, combos, i, result):
    try:
        for letter in groups[i]:
            result[i] = letter
            comboGen(groups, combos, i + 1, result)
    except IndexError:
        combos.append(''.join(result))
        return
