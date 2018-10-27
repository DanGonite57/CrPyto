import importlib

imports = [
    "Ciphers",
    "Formatting",
    "Processing"
]

for each in imports:
    importlib.import_module("." + each, __package__)

del importlib
