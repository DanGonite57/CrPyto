# -*- coding: utf-8 -*-

"""
Formatting.Format
~~~~~~~~~~~~~~~~~

This module implements various processes for text manipulation.
"""

from string import ascii_letters as ALPH


def remove(text, *args):
    """
    Remove certain characters from text.

    :param args: list of characters to be removed
    """

    chars = ''.join(args)
    for char in chars:
        text = text.replace(char, "")

    return text


def keepOnly(text, *args):
    """
    Remove all characters except those specified.

    :param args: list of characters to be kept
    """

    chars = ''.join(args)
    new = ""
    for char in text:
        if char in chars:
            new += char

    return new


def readd(new, old):
    """Add non-alphabetic characters back into manipulated text."""

    new = [x for x in new]
    for i, char in enumerate(old):
        if char not in ALPH:
            try:
                if new[i] != char:
                    new.insert(i, char)
            except IndexError:
                new.append(char)

    return ''.join(new)
