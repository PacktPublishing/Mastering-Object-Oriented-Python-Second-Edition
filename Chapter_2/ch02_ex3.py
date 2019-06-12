#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 2. Example 3.
"""

from Chapter_2.ch02_ex2 import *
from typing import cast, Iterable, Iterator

# Factory Function


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


# This function builds a Card from a numeric rank and a Suit object. We can now # build cards very simply.

test_card = """
    >>> deck = [card(rank, suit) for rank in range(1, 14) for suit in (Suit.Club, Suit.Diamond, Suit.Heart, Suit.Spade)]
    >>> len(deck)
    52
    >>> sorted(set(c.suit for c in deck))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

deck = [
    card(rank, suit) for rank in range(1, 14) for suit in cast(Iterable[Suit], Suit)
]
deck_l = [
    card(rank, suit) for rank in range(1, 14) for suit in iter(Suit)
]


# Here's a less desirable form of the factory function.
# It harbors a hidden bug because the else assumes too much.


def card2(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    else:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)


test_card2 = """
    >>> deck2 = [card2(rank, suit) for rank in range(13) for suit in Suit]  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    KeyError: 0
"""

# Here's a more consistent factory function that doesn't mix elif and a mapping.


def card3(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif rank == 11:
        return FaceCard("J", suit)
    elif rank == 12:
        return FaceCard("Q", suit)
    elif rank == 13:
        return FaceCard("K", suit)
    else:
        raise Exception("Rank out of range")


# Note... This works, but mypy doesn't completely understand the simple form.
# To help mypy, we use this: cast(Iterable[Suit], Suit)
# This makes it clear an Enum subclass is an iterable over the enumerated values.

test_card3 = """
    >>> deck3 = [card3(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> len(deck3)
    52
    >>> sorted(set(c.suit for c in deck3))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck3))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

deck3 = [
    card3(rank, suit) for rank in range(1, 14) for suit in cast(Iterable[Suit], Suit)
]


# Here's an incomplete, but more consistent factory that uses just a mapping.
# This doesn't properly translate rank to a string.


def card4(rank: int, suit: Suit) -> Card:
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    return class_(str(rank), suit)


test_card4 = """
    >>> deck4 = [card4(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> len(deck4)
    52
    >>> sorted(set(c.suit for c in deck4))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck4))
    ['1', '10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']
"""

# Here's the two-parallel mapping version.


def card5(rank: int, suit: Suit) -> Card:
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))
    return class_(rank_str, suit)


test_card5 = """
    >>> deck5 = [card5(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> len(deck5)
    52
    >>> sorted(set(c.suit for c in deck5))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck5))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

# Here's the mapping two a 2-tuple version.


def card6(rank: int, suit: Suit) -> Card:
    class_, rank_str = {
        1: (AceCard, "A"), 11: (FaceCard, "J"), 12: (FaceCard, "Q"), 13: (FaceCard, "K")
    }.get(
        rank, (Card, str(rank))
    )
    return class_(rank_str, suit)


test_card6 = """
    >>> deck6 = [card6(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> len(deck6)
    52
    >>> sorted(set(c.suit for c in deck6))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck6))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

# Here's the mapping to a partial version.

# While this is appealing, it doesn't work well for class instance creation.
# We get TypeError: 'AceCard' object is not callable

# from functools import partial
# part_class = partial(AceCard, 'A')
# card = part_class(Suit.Heart)

# Instead, we'll use lambdas as our partials.


def card7(rank: int, suit: Suit) -> Card:
    class_rank = {
        1: lambda suit: AceCard("A", suit),
        11: lambda suit: FaceCard("J", suit),
        12: lambda suit: FaceCard("Q", suit),
        13: lambda suit: FaceCard("K", suit),
    }.get(
        rank, lambda suit: Card(str(rank), suit)
    )
    return class_rank(suit)


test_card7 = """
    >>> deck7 = [card7(rank, suit) for rank in range(1, 14) for suit in Suit]
    >>> len(deck7)
    52
    >>> sorted(set(c.suit for c in deck7))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck7))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

# Here's a stateful card factory that uses a fluent interface
# to build cards. Note the methods **must** be called in the right
# order, a common limitation of fluent interfaces.


class CardFactory:

    def rank(self, rank: int) -> "CardFactory":
        self.class_, self.rank_str = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K"),
        }.get(
            rank, (Card, str(rank))
        )
        return self

    def suit(self, suit: Suit) -> Card:
        return self.class_(self.rank_str, suit)


test_card8 = """
    >>> card8 = CardFactory()
    >>> deck8 = [card8.rank(r + 1).suit(s) for r in range(13) for s in Suit]
    >>> len(deck8)
    52
    >>> sorted(set(c.suit for c in deck8))
    [<Suit.Spade: '♠'>, <Suit.Club: '♣'>, <Suit.Heart: '♥'>, <Suit.Diamond: '♦'>]
    >>> sorted(set(c.rank for c in deck8))
    ['10', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q']
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)

    deck = [
        card(rank, suit) for rank in range(1, 14) for suit in cast(Iterable[Suit], Suit)
    ]
    deck3 = [
        card3(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterable[Suit], Suit)
    ]
    deck4 = [
        card4(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterable[Suit], Suit)
    ]
    deck5 = [
        card5(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterable[Suit], Suit)
    ]
    deck6 = [
        card6(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterable[Suit], Suit)
    ]
    deck7 = [
        card7(rank, suit)
        for rank in range(1, 14)
        for suit in cast(Iterable[Suit], Suit)
    ]
    card8 = CardFactory()
    deck8 = [
        card8.rank(r + 1).suit(s) for r in range(13) for s in cast(Iterable[Suit], Suit)
    ]
