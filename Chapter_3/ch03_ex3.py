#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 3. Example 3.
"""

import sys
import random
from typing import cast, Iterable, Any, Callable
from Chapter_3.ch03_ex1 import Suit, Card2, card2

# Complex Mutable Object Example
# ==============================

# Definition of a simple class hierarchy
# with a formal equality and hash test.


class Hand:

    def __init__(self, dealer_card: Card2, *cards: Card2) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ", ".join(map(repr, self.cards))
        return f"{self.__class__.__name__}({self.dealer_card!r}, {cards_text})"

    def __format__(self, spec: str) -> str:
        if spec == "":
            return str(self)
        return ", ".join(f"{c:{spec}}" for c in self.cards)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == other
        try:
            return (
                self.cards == cast(Hand, other).cards
                and self.dealer_card == cast(Hand, other).dealer_card
            )
        except AttributeError:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() < other
        try:
            return self.total() < cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() <= other
        try:
            return self.total() <= cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    # __hash__: Callable[[], int] = None

    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard = sum(c.hard for c in self.cards)
        if hard + delta_soft <= 21:
            return hard + delta_soft
        return hard


class FrozenHand(Hand):

    def __init__(self, *args, **kw) -> None:
        if len(args) == 1 and isinstance(args[0], Hand):
            # Clone a hand
            other = cast(Hand, args[0])
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh Hand from Card instances.
            super().__init__(*args, **kw)

    def __hash__(self) -> int:
        return sum(hash(c) for c in self.cards) % sys.hash_info.modulus


class Deck(list):

    def __init__(self) -> None:
        super().__init__(
            card2(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit)
        )
        random.shuffle(self)


test_frozen_hand = """
    >>> from collections import defaultdict
    >>> random.seed(1138)
    >>> d = Deck()
    >>> h = Hand(d.pop(), d.pop(), d.pop())
    
    >>> print("Player: {hand:%r%s}".format(hand=h))
    Player: K♦, 9♥

    >>> stats = defaultdict(int)
    >>> stats[h] += 1  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: unhashable type: 'Hand'
    
    
    >>> h_f = FrozenHand(h)
    >>> stats = defaultdict(int)
    >>> stats[h_f] += 1
    >>> print(stats)
    defaultdict(<class 'int'>, {FrozenHand(NumberCard2(suit=<Suit.Heart: '♥'>, rank='5'), FaceCard2(suit=<Suit.Diamond: '♦'>, rank='K'), NumberCard2(suit=<Suit.Heart: '♥'>, rank='9')): 1})
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
