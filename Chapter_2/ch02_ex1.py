#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 2. Example 1.
"""
from typing import Tuple


class Card:

    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class AceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 10, 10


test_card = """
    >>> x = Card('2','♠')
    >>> str(x)  # doctest: +ELLIPSIS
    '<....Card object at ...>'
    >>> repr(x)  # doctest: +ELLIPSIS
    '<....Card object at ...>'
    >>> print(x)  # doctest: +ELLIPSIS
    <....Card object at ...>
    >>> cards = [AceCard('A', '♠'), Card('2','♠'), FaceCard('J','♠'),]
    >>> cards  # doctest: +ELLIPSIS
    [<...AceCard ...>, <...Card ...>, <...FaceCard ...>]
    
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
