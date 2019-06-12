#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 3. Example 1.
"""

from typing import Any, cast, Callable
from enum import Enum
import sys

# Mutable and Immutable Objects
# ==============================

# Card Class with anomalies
# ############################

# Definition of a simple class hierarchy for immutable objects
# without a formal equality test or hash function. This will
# somewhat work as expected. However, there will also be anomalies.


class Card:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class NumberCard(Card):

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard(Card):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard(Card):

    def __init__(self, rank: int, suit: "Suit") -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


class Suit(str, Enum):
    Club = "\N{BLACK CLUB SUIT}"
    Diamond = "\N{BLACK DIAMOND SUIT}"
    Heart = "\N{BLACK HEART SUIT}"
    Spade = "\N{BLACK SPADE SUIT}"


# Some Use cases for two seemingly equal cards.

test_card = """
    >>> c1 = AceCard(1, Suit.Club)
    >>> c2 = AceCard(1, Suit.Club)

    >>> id(c1) == id(c2)
    False
    >>> c1 is c2
    False
    >>> hash(c1) == hash(c2)
    False
    >>> hash(c1), hash(c2)  # doctest: +ELLIPSIS
    (..., ...)
    >>> c1 == c2
    False
    >>> set([c1, c2])
    {AceCard(suit=<Suit.Club: '♣'>, rank='A'), AceCard(suit=<Suit.Club: '♣'>, rank='A')}
"""

# Better Card Class
# ############################

# Definition of a more sophisticated class hierarchy
# with a formal equality and hash test. This will create
# properly immutable objects. There will be no anomalies with
# seemingly equal objects.

# We'll look at a far better solution using typing.NamedTuple below.


class Card2:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast(Card2, other).suit
            and self.rank == cast(Card2, other).rank
        )

    def __hash__(self) -> int:
        return (hash(self.suit) + 4*hash(self.rank)) % sys.hash_info.modulus

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return str(self)
        rs = (
            format_spec.replace("%r", self.rank)
                       .replace("%s", self.suit)
                       .replace("%%", "%")
        )
        return rs

    def __bytes__(self) -> bytes:
        class_code = self.__class__.__name__[0]
        rank_number_str = {"A": "1", "J": "11", "Q": "12", "K": "13"}.get(
            self.rank, self.rank
        )
        string = f"({' '.join([class_code, rank_number_str, self.suit])})"
        return bytes(string, encoding="utf-8")


class NumberCard2(Card2):

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard2(Card2):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard2(Card2):

    def __init__(self, rank: int, suit: "Suit") -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


def card2(rank: int, suit: Suit) -> Card2:
    class_ = {1: AceCard2, 11: FaceCard2, 12: FaceCard2, 13: FaceCard2}.get(
        rank, NumberCard2
    )
    return class_(rank, suit)


# Some Use cases for two seemingly equal cards.

test_card2 = """
    >>> c1 = AceCard2(1, Suit.Club)
    >>> c2 = AceCard2(1, Suit.Club)

    >>> id(c1), id(c2)  # doctest: +ELLIPSIS
    (..., ...)

    >>> id(c1) == id(c2)
    False
    >>> c1 is c2
    False
    >>> hash(c1) == hash(c2)
    True
    >>> c1 == c2
    True
    >>> set([c1, c2])
    {AceCard2(suit=<Suit.Club: '♣'>, rank='A')}
    
    >>> bytes(c1)
    b'(A 1 \xe2\x99\xa3)'
"""


# Another Poorly-Designed Card Class
# ##################################

# Definition of a weird class hierarchy
# with a formal equality but no hash test. This will create
# properly mutable objects that can't be put into sets.


class Card3:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast(Card3, other).suit
            and self.rank == cast(Card3, other).rank
        )

    # __hash__ = None  # mypy balks at this.


class AceCard3(Card3):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class NumberCard3(Card3):

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__(str(rank), suit, rank, rank)


class FaceCard3(Card3):

    def __init__(self, rank: int, suit: "Suit") -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


# Some Use cases for two seemingly equal cards that cannot be hashed.

test_card3 = """
    >>> c1 = AceCard3(1, Suit.Club)
    >>> c2 = AceCard3(1, Suit.Club)

    >>> id(c1) == id(c2)
    False
    >>> c1 is c2
    False
    >>> hash(c1) == hash(c2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: unhashable type: 'AceCard3'
    >>> c1 == c2
    True
    >>> set([c1, c2])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: unhashable type: 'AceCard3'
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
