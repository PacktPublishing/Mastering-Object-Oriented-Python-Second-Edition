#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 4. Example 2.
"""
import random
from typing import List

from Chapter_4.ch04_ex1 import Deck, BlackJackCard


# Property Decorator
# ==============================
#
# Definition of Hand using a property for the total.


class Hand:

    def __init__(
            self,
             dealer_card: BlackJackCard,
             *cards: BlackJackCard
        ) -> None:
        self.dealer_card: BlackJackCard = dealer_card
        self._cards: List[BlackJackCard] = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.card))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}, " 
            f"{', '.join(map(repr, self.card))})"
        )

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, aCard: BlackJackCard) -> None:
        raise NotImplementedError

    @card.deleter
    def card(self) -> None:
        raise NotImplementedError

    def split(self, deck: Deck) -> "Hand":
        """Updates this hand and also returns the new hand."""
        assert self._cards[0].rank == self._cards[1].rank
        c1 = self._cards[-1]
        del self.card
        self.card = deck.pop()
        h_new = self.__class__(self.dealer_card, c1, deck.pop())
        return h_new


class Hand_Lazy(Hand):

    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self._cards)
        hard_total = sum(c.hard for c in self._cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft
        return hard_total

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, aCard: BlackJackCard) -> None:
        self._cards.append(aCard)

    @card.deleter
    def card(self) -> None:
        self._cards.pop(-1)


# We can now work with the total value of a hand using Hand.total
# instead of hand.total().
#


test_hand_lazy = """
    >>> random.seed(9973)
    >>> d = Deck()
    >>> h = Hand_Lazy(d.pop(), d.pop(), d.pop())
    >>> print(h.total)
    14
    >>> h.card = d.pop()
    >>> print(h.total)
    18
"""

# What's the advantage?
# Simpler syntax. We can still have lazy vs. eager calculation of
# the total value of the hand.


class Hand_Eager(Hand):

    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard
    ) -> None:
        self.dealer_card = dealer_card
        self.total = 0
        self._delta_soft = 0
        self._hard_total = 0
        self._cards: List[BlackJackCard] = list()
        for c in cards:
            # Mypy cannot discern the actual type of the setter.
            # https://github.com/python/mypy/issues/4167
            self.card = c  # type: ignore

    @property
    def card(self) -> List[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, aCard: BlackJackCard) -> None:
        self._cards.append(aCard)
        self._delta_soft = max(aCard.soft - aCard.hard, self._delta_soft)
        self._hard_total = self._hard_total + aCard.hard
        self._set_total()

    @card.deleter
    def card(self) -> None:
        removed = self._cards.pop(-1)
        self._hard_total -= removed.hard
        # Issue: was this the only ace?
        self._delta_soft = max(c.soft - c.hard for c in self._cards)
        self._set_total()

    def _set_total(self) -> None:
        if self._hard_total + self._delta_soft <= 21:
            self.total = self._hard_total + self._delta_soft
        else:
            self.total = self._hard_total


test_hand_eager_and_lazy = """
    >>> random.seed(9973)
    >>> d = Deck()
    >>> h = Hand_Eager(d.pop(), d.pop(), d.pop())
    >>> print(h.total)
    14
    >>> h.card = d.pop()
    >>> print(h.total)
    18

    >>> random.seed(9973)
    >>> d = Deck()
    >>> c = d.pop()
    >>> h = Hand_Lazy(d.pop(), c, c)  # Force splittable hand
    >>> h2 = h.split(d)

    >>> print(h)
    6♦, A♦
    >>> print(h2)
    6♦, 4♠
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
