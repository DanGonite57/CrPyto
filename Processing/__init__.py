import importlib

imports = [
    "Decrypt",
    "DetectEnglish",
    "PatternGen"
]

for each in imports:
    importlib.import_module("." + each, __package__)

del importlib
