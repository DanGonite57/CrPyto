import collections
import itertools
import string

from Processing import DetectEnglish

ALPH = string.ascii_lowercase


def decrypt(ciph, factors=None):
    ciph = ciph.lower()
    if not factors:

        # Find repeats
        sub = {}
        for subLength in range(3, len(ciph)):  # May need to switch back to range(3, len(ciph))
            for i in range(len(ciph) - subLength + 1):
                try:
                    sub[ciph[i: i + subLength]].append(i)
                except KeyError:
                    sub[ciph[i: i + subLength]] = [i]

        # Remove non-dupes
        sub = {key: sub[key] for key in sub if len(sub[key]) != 1}

        # Get possible key lengths
        keylens = []
        for key in sub:
            for i in range(len(sub[key]) - 1):
                keylens.append(sub[key][i + 1] - sub[key][i])

        # Get keylength factors
        factors = []
        for i in keylens:
            factors += getFactors(i)
        factors = [x[0] for x in collections.Counter(factors).most_common() if x[1] == collections.Counter(factors).most_common(1)[0][1]]

    else:
        factors = [factors]

    # Get substrings
    allResults = []
    for n in factors:

        substrings = []
        keycombos = []
        newsubs = {}

        for i in range(n):
            substring = ''.join([ciph[x] for x in range(i, len(ciph), n)])
            substrings.append(substring)

            # Get substring-english similarity
            newsubs[i] = {}
            poss = []
            for j in range(26):
                new = ""
                shift = ALPH[-j::] + ALPH[:-j]
                for l in substring:
                    new += (shift[ALPH.index(l)])
                poss.append((ALPH[j], DetectEnglish.freqMatch(''.join(new))))
                newsubs[i][ALPH[j]] = new

            # Get most likely substring(s)
            bestFreq = 0
            keys = []
            for x in poss:
                if x[1] > bestFreq:
                    bestFreq = x[1]
                    keys = []
                    keys.append(x[0])
                elif x[1] == bestFreq:
                    keys.append(x[0])
            keycombos.append(keys)

        # Create combinations
        combos = []
        comboGen(keycombos, combos, 0, [[]] * len(keycombos))
        # Merge keystrings
        results = []
        for combo in combos:
            keystrings = []
            for i, x in enumerate(combo):
                keystrings.append(newsubs[i][x])
            results.append(''.join([''.join(x) for x in itertools.zip_longest(*keystrings, fillvalue="")]))

        # Test result for englishness
        result, score = DetectEnglish.getBest(results)
        allResults.append(result)

    results, score = DetectEnglish.getBest(allResults)

    return result, score


def getFactors(n):
    return [i for i in range(2, n + 1) if n % i == 0]


def comboGen(groups, combos, i, result):
    """Create all possible combinations of a limited set"""
    try:
        for letter in groups[i]:
            result[i] = letter
            comboGen(groups, combos, i + 1, result)
    except IndexError:
        combos.append(''.join(result))
        return
