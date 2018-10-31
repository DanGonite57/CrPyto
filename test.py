from Ciphers import Vigenere

# print(Vigenere.decrypt("DLCCMEXWUOVCCYZDPCKRBSXRYSIWIYGLGVIRYWNYXRRIKLYRQVYNYYVPWSWRKVROHRYQYUIRRIKYYRKRBVMIOSLOSDDLMCIMVHDKWFSSLOHBZMADYPOWRRERCTPSRECMLDSDYGSCAFORWYYABSQCCMEVCIIQKRBMSSXXRYEFERBBIBDLCDVSDLABCQDEJVMQOHYXHGBIYVMQOHRRERSLYNFCORQOEPMLGXKDYVGDEJVEJYRESXUKWLDXFKXGPSSXHQYQCDLGXKNKVRSGSVEPGLYDMLYXGMIBGEQKGREEJVCYXEZCILMIYGLMVIAYPJOGRSSLYJYZTYBILDPWERPOPYDIBDLGXKQDLYDWFYYJNLYFICHMQDIBLYRNMBXXYXHHEWRKWGREBPMEEVCNXFKXMEXQYQCYRCKRBLEAUXFORGNMBXXIXSUGLMGVMDIRYXCVPKOEZYYRSXRRIWYFTSSSCPWREBKWCXWCYJRRIBBEKKXGMELNELOBAOPJORRCILCIMPXGWMLQMDDLCILYNWCXXGDXMWICFILKJCGHYIWZOJMBIGGSSVHFKZCKWQEQCNMRGEQCSKOOGXHMPGPKDWKHTOVRSWGXKQDYLDFSDAFORRRINYWRMEPNEPBMTOHGDAYCMKWIBSEROPWYFTSSSCXMWIURERSXPOJCBVCNXMSXAKVPSIBTYQDXFBICGSPNWYXHGDHCCGPSFCNTCBJCMXJIXFOQGCWGXKNSIAOWGXQWZYXJPCSXHEWRCEGNXFOWFKHMGEPMLGFI"))

print(Vigenere.decrypt("PPQCAXQVEKGYBNKMAZUYBNGBALJONITSZMJYIMVRAGVOHTVRAUCTKSGDDWUOXITLAZUVAVVRAZCVKBQPIWPOUjwdppgxppgizqgnwvkgwansgmqropkdebjkoipyomcxzbjolwnsymcbnqxozpk"))

# groups = {1: ['q', 'h', 'z'], 2: ['w', 'f'], 3: ['c', 'a']}


# def comboGen(unsolved, combos, keys, i, vals):
#     try:
#         for letter in unsolved[keys[i]]:
#             # Adds a possible letter to combo
#             vals[keys[i]] = letter
#             # Moves to next key
#             comboGen(unsolved, combos, keys, i + 1, vals)
#     except IndexError:
#         # Where the end of the list of keys is reached
#         combo = ""
#         for char in keys:
#             # Create combo string
#             combo += vals[char]
#         combos.append(combo)
#         return

# combos = []
# comboGen(groups, combos, sorted(groups.keys()), 0, {})
# print(combos)

# groups = [['q', 'h', 'z'], ['w', 'f'], ['c', 'a']]


# def comboGen(groups, combos, i, result):
#     try:
#         for letter in groups[i]:
#             result[i] = letter
#             comboGen(groups, combos, i + 1, result)
#     except IndexError:
#         combos.append(''.join(result))
#         return

# combos = []
# comboGen(groups, combos, 0, [[]] * len(groups))
# print(combos)
