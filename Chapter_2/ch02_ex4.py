#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 2. Example 4.
"""

# Alternative Designs for the Initialization

from Chapter_2.ch02_ex3 import card, Suit
from typing import Any, cast, Iterator
from abc import abstractmethod

# Subclass only. Omitting the superclass __init__, while legal, baffles mypy badly.
# Omitting the __init__ is not suggested.


class Card2:

    @abstractmethod
    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank: str
        self.suit: Suit
        self.hard: int
        self.soft: int

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast("Card2", other).suit
            and self.rank == cast("Card2", other).rank
            and self.hard == cast("Card2", other).hard
            and self.soft == cast("Card2", other).soft
        )

    def __repr__(self) -> str:
        return f"suit={self.suit!r}, rank={self.rank!r}, hard={self.hard!r}, soft={self.soft!r}"


class NumberCard2(Card2):

    def __init__(self, rank: int, suit: Suit) -> None:
        self.suit = suit
        self.rank = str(rank)
        self.hard = self.soft = rank


class AceCard2(Card2):

    def __init__(self, rank: int, suit: Suit) -> None:
        self.suit = suit
        self.rank = "A"
        self.hard, self.soft = 1, 11


class FaceCard2(Card2):

    def __init__(self, rank: int, suit: Suit) -> None:
        self.suit = suit
        self.rank = {11: "J", 12: "Q", 13: "K"}[rank]
        self.hard = self.soft = 10


def card9(rank: int, suit: Suit) -> Card2:
    if rank == 1:
        return AceCard2(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard2(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard2(rank, suit)
    else:
        raise Exception("Rank out of range")


test_compare_card9_with_card = """
    >>> # Compare with an example 2 deck
    >>> deck = [card(rank, suit) for rank in range(1, 14) for suit in (Suit.Club, Suit.Diamond, Suit.Heart, Suit.Spade)]
    >>> deck9 = [card9(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> for c9, c in zip(deck9, deck):
    ...    assert c9 == c, f"{c9!r} != {c!r}"
    >>> assert deck9 == deck
"""

# Mixed subclass and superclass.

# It's abstract in principle, but technically concrete.
# This parallels a dataclass.


class Card3:

    def __init__(self, rank: str, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast("Card3", other).suit
            and self.rank == cast("Card3", other).rank
            and self.hard == cast("Card3", other).hard
            and self.soft == cast("Card3", other).soft
        )


class NumberCard3(Card3):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard3(Card3):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard3(Card3):

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


def card10(rank: int, suit: Suit) -> Card3:
    if rank == 1:
        return AceCard3(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard3(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard3(rank, suit)
    else:
        raise Exception("Rank out of range")


test_compare_card10_with_card = """
    >>> # Compare with an example 2 deck
    >>> deck = [card(rank, suit) for rank in range(1, 14) for suit in (Suit.Club, Suit.Diamond, Suit.Heart, Suit.Spade)]
    >>> deck10 = [card10(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> assert deck10 == deck
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)

    deck9 = [
        card9(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterator[Suit], Suit)
    ]
    deck10 = [
        card10(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterator[Suit], Suit)
    ]
