import importlib

imports = [
    "Caesar",
    "Substitution",
    "Transposition",
    "Vigenere"
]

for each in imports:
    importlib.import_module("." + each, __package__)

del importlib
