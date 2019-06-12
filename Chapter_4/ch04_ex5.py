#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 4. Example 5.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, cast, Iterable, Optional


@dataclass
class RTD:
    rate: Optional[float]
    time: Optional[float]
    distance: Optional[float]

    def compute(self) -> "RTD":
        if (
            self.distance is None and self.rate is not None and self.time is not None
        ):
            self.distance = self.rate * self.time
        elif (
            self.rate is None and self.distance is not None and self.time is not None
        ):
            self.rate = self.distance / self.time
        elif (
            self.time is None and self.distance is not None and self.rate is not None
        ):
            self.time = self.distance / self.rate
        return self


test_rtd = """
    >>> r = RTD(distance=13.5, rate=6.1, time=None)
    >>> r.compute()
    RTD(rate=6.1, time=2.2131147540983607, distance=13.5)
"""


class Suit(str, Enum):
    Club = "\N{BLACK CLUB SUIT}"
    Diamond = "\N{BLACK DIAMOND SUIT}"
    Heart = "\N{BLACK HEART SUIT}"
    Spade = "\N{BLACK SPADE SUIT}"


@dataclass(frozen=True, order=True)
class Card:
    rank: int
    suit: str

    @property
    def points(self) -> int:
        return self.rank


class Ace(Card):

    @property
    def points(self) -> int:
        return 1


class Face(Card):

    @property
    def points(self) -> int:
        return 10


def deck() -> Iterator[Card]:
    for rank in range(1, 14):
        for suit in cast(Iterable[Suit], Suit):
            if rank == 1:
                yield Ace(rank, suit)
            elif rank >= 11:
                yield Face(rank, suit)
            else:
                yield Card(rank, suit)


test_dataclass = """
    >>> a = Card(7, Suit.Heart)
    >>> a.rank
    7
    >>> a.suit
    <Suit.Heart: '♥'>
    >>> b = Card(7, Suit.Heart)
    >>> a == b
    True
    >>> a < Card(8, Suit.Spade)
    True
"""

test_hand = """
    >>> import random
    >>> random.seed(16)
    >>> cards = list(deck())
    >>> random.shuffle(cards)
    >>> hand = cards[:5]
    >>> any(c.rank == 1 for c in hand)
    True
    >>> any(c.points == 10 for c in hand)
    True
    >>> sum(c.points for c in hand)
    34
    >>> for c in hand:
    ...     print(f"{c!r}: {c.points}")
    Card(rank=3, suit=<Suit.Heart: '♥'>): 3
    Ace(rank=1, suit=<Suit.Spade: '♠'>): 1
    Face(rank=11, suit=<Suit.Club: '♣'>): 10
    Face(rank=13, suit=<Suit.Spade: '♠'>): 10
    Face(rank=12, suit=<Suit.Diamond: '♦'>): 10
    >>> Ace(1, Suit.Spade) in set(hand)
    True
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
