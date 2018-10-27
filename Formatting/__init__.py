import importlib

imports = [
    "SpaceRem",
    "PuncRem"
]

for each in imports:
    importlib.import_module("." + each, __package__)

del importlib
