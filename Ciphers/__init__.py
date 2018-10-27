import importlib

imports = [
    "Caesar",
    "Substitution",
    "Transposition"
]

for each in imports:
    importlib.import_module("." + each, __package__)

del importlib
