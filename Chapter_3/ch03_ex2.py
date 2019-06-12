#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 3. Example 2.
"""

from typing import NamedTuple, Tuple, cast, Iterable
from enum import Enum

# Properly Immutable Card
# =======================


class Suit(str, Enum):
    Club = "\N{BLACK CLUB SUIT}"
    Diamond = "\N{BLACK DIAMOND SUIT}"
    Heart = "\N{BLACK HEART SUIT}"
    Spade = "\N{BLACK SPADE SUIT}"


class Card(NamedTuple):
    rank: str
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit.value}"

    @property
    def insure(self) -> bool:
        return False

    @property
    def hard(self) -> int:
        hard, soft = self._points()
        return hard

    @property
    def soft(self) -> int:
        hard, soft = self._points()
        return soft

    def _points(self) -> Tuple[int, int]:
        pass


class NumberCard(Card):

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class AceCard(Card):

    @property
    def insure(self) -> bool:
        return True

    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 10, 10


def card(rank: int, suit: Suit) -> Card:
    class_, rank_str = {
        1: (AceCard, "A"), 11: (FaceCard, "J"), 12: (FaceCard, "Q"), 13: (FaceCard, "K")
    }.get(
        rank, (NumberCard, str(rank))
    )
    return class_(rank_str, suit)


test_card = """
    >>> deck = [card(r, s) for r in range(1, 14) for s in cast(Iterable[Suit], Suit)]
    >>> len(deck)
    52
    >>> s_1 = card(1, Suit.Spade)
    >>> s_1
    AceCard(rank='A', suit=<Suit.Spade: '♠'>)
    >>> s_1.insure
    True
    >>> s_1.hard
    1
    >>> s_1.soft
    11
    >>> s_j = card(11, Suit.Spade)
    >>> s_j
    FaceCard(rank='J', suit=<Suit.Spade: '♠'>)
    >>> s_j.insure
    False
    >>> s_j.hard
    10
    >>> s_j.soft
    10
"""

# Some Use cases for two seemingly equal cards.

test_card_equality = """
    >>> c1 = card(1, Suit.Club)
    >>> c2 = card(1, Suit.Club)

    >>> id(c1) == id(c2)
    False
    >>> c1 is c2
    False
    >>> hash(c1) == hash(c2)
    True
    >>> c1 == c2
    True
    >>> set([c1, c2])
    {AceCard(rank='A', suit=<Suit.Club: '♣'>)}
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
