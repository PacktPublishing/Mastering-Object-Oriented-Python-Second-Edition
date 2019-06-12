#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 2. Example 2.
"""

from typing import Tuple, Any, Union, cast

# Definition of a simple class hierarchy.
# Note the overlap with a dataclass if we use properties.


class Card:
    insure = False

    def __init__(self, rank: str, suit: Any) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast("Card", other).suit
            and self.rank == cast("Card", other).rank
            and self.hard == cast("Card", other).hard
            and self.soft == cast("Card", other).soft
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class AceCard(Card):
    insure = True

    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 10, 10


# We can create cards like this

test_card = """
    >>> Suit.Club
    <Suit.Club: '♣'>
    >>> d1 = [AceCard('A', '♠'), Card('2', '♠'), FaceCard('Q', '♠'), ]
    >>> d1
    [AceCard(suit='♠', rank='A'), Card(suit='♠', rank='2'), FaceCard(suit='♠', rank='Q')]
    >>> Card('2', '♠')
    Card(suit='♠', rank='2')
    >>> str(Card('2', '♠'))
    '2♠'
"""

# Instead of strings, we can use an enum

from enum import Enum


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


# We can create cards like this

test_card_suit = """
    >>> cards = [AceCard('A', Suit.Spade), Card('2', Suit.Spade), FaceCard('Q', Suit.Spade),]
    >>> cards
    [AceCard(suit=<Suit.Spade: '♠'>, rank='A'), Card(suit=<Suit.Spade: '♠'>, rank='2'), FaceCard(suit=<Suit.Spade: '♠'>, rank='Q')]
"""

test_suit_value = """
    >>> Suit.Heart.value
    '♥'
    >>> Suit.Heart.value = 'H'  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_suit_value[1]>", line 1, in <module>
        Suit.Heart.value = 'H'
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/types.py", line 175, in __set__
        raise AttributeError("can't set attribute")
    AttributeError: can't set attribute
    
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
