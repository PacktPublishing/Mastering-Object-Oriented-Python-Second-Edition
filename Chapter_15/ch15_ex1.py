#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 15. Example 1.
"""
import random
from typing import Tuple, List, Iterator, Optional, Type

# A poor design


class DominoBoneYard:
    """
    A relatively poor design. A number of unrelated things all jumbled
    together

    >>> random.seed(42)
    >>> dby = DominoBoneYard()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [(5, 3), (5, 1), (4, 0), (6, 0), (6, 6), (3, 0), (2, 2)]
    >>> dby.score_hand(hands[0])
    43
    >>> hands[1]
    [(4, 1), (4, 4), (3, 3), (6, 3), (4, 2), (5, 4), (5, 0)]
    >>> dby.rank_hand(hands[1])
    >>> dby.score_hand(hands[1][-2:])
    10
    >>> hands[2]
    [(6, 4), (1, 0), (4, 3), (1, 1), (5, 2), (6, 5), (2, 1)]
    >>> dby.doubles_indices(hands[0])
    [4, 6]
    >>> for d in  dby.doubles_indices(hands[0]):
    ...     print(hands[0][d])
    (6, 6)
    (2, 2)
    >>> dby.can_play_first(hands[0])
    True
    """

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def double(self, domino: Tuple[int, int]) -> bool:
        x, y = domino
        return x == y

    def score(self, domino: Tuple[int, int]) -> int:
        return domino[0] + domino[1]

    def hand_iter(self, players: int = 4) -> Iterator[List[Tuple[int, int]]]:
        for p in range(players):
            yield self._dominoes[p * 7:p * 7 + 7]

    def can_play_first(self, hand: List[Tuple[int, int]]) -> bool:
        for d in hand:
            if self.double(d) and d[0] == 6:
                return True
        return False

    def score_hand(self, hand: List[Tuple[int, int]]) -> int:
        return sum(d[0] + d[1] for d in hand)

    def rank_hand(self, hand: List[Tuple[int, int]]) -> None:
        hand.sort(key=self.score, reverse=True)

    def doubles_indices(self, hand: List[Tuple[int, int]]) -> List[int]:
        return [i for i in range(len(hand)) if self.double(hand[i])]


# Revised and Decomposed based on ISP
from typing import NamedTuple


class Domino(NamedTuple):
    v1: int
    v2: int

    def double(self) -> bool:
        return self.v1 == self.v2

    def score(self) -> int:
        return self.v1 + self.v2


class Hand(list):

    def score(self) -> int:
        return sum(d.score() for d in self)

    def rank(self) -> None:
        self.sort(key=lambda d: d.score(), reverse=True)

    def doubles_indices(self) -> List[int]:
        return [i for i in range(len(self)) if self[i].double()]


class DominoBoneYard2:

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [Domino(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        for p in range(players):
            hand, self._dominoes = Hand(self._dominoes[:7]), self._dominoes[7:]
            yield hand


test_dby2 = """
    >>> random.seed(42)
    >>> dby = DominoBoneYard2()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hands[1]
    [Domino(v1=4, v2=1), Domino(v1=4, v2=4), Domino(v1=3, v2=3), Domino(v1=6, v2=3), Domino(v1=4, v2=2), Domino(v1=5, v2=4), Domino(v1=5, v2=0)]
    >>> hands[1].rank()
    >>> hands[1].pop(0)
    Domino(v1=6, v2=3)
    >>> hands[1].pop(0)
    Domino(v1=5, v2=4)
    >>> hands[1].pop(0)
    Domino(v1=4, v2=4)
    >>> hands[1].pop(0)
    Domino(v1=3, v2=3)
    >>> hands[1].pop(0)
    Domino(v1=4, v2=2)
    >>> hands[1].score()
    10
    >>> hands[2]
    [Domino(v1=6, v2=4), Domino(v1=1, v2=0), Domino(v1=4, v2=3), Domino(v1=1, v2=1), Domino(v1=5, v2=2), Domino(v1=6, v2=5), Domino(v1=2, v2=1)]
    >>> hands[0].doubles_indices()
    [4, 6]
    >>> for d in hands[0].doubles_indices():
    ...     print(hands[0][d])
    Domino(v1=6, v2=6)
    Domino(v1=2, v2=2)
"""


class Hand3(Hand):

    def highest_double_index(self) -> Optional[int]:
        descending = sorted(
            self.doubles_indices(),
            key=lambda double_index: self[double_index].v1,
            reverse=True,
        )
        if descending:
            return descending[0]
        return None


class DominoBoneYard3(DominoBoneYard2):

    def hand_iter(self, players: int = 4) -> Iterator[Hand3]:
        for p in range(players):
            hand, self._dominoes = Hand3(self._dominoes[:7]), self._dominoes[7:]
            yield hand


test_dby3 = """
    >>> random.seed(42)
    >>> dby = DominoBoneYard3()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hdi = hands[0].highest_double_index()
    >>> hdi
    4
    >>> hands[0][hdi]
    Domino(v1=6, v2=6)
    >>> hands[1]
    [Domino(v1=4, v2=1), Domino(v1=4, v2=4), Domino(v1=3, v2=3), Domino(v1=6, v2=3), Domino(v1=4, v2=2), Domino(v1=5, v2=4), Domino(v1=5, v2=0)]
"""


class FancyDealer4:

    def __init__(self):
        self.boneyard = DominoBoneYard3()

    def hand_iter(
        self, players: int = 4, tiles: int = 7
    ) -> Iterator[Hand3]:
        if players * tiles > len(self.boneyard._dominoes):
            raise ValueError(f"Can't deal players={players} tiles={tiles}")
        for p in range(players):
            hand = Hand3(self.boneyard._dominoes[:tiles])
            self.boneyard._dominoes = self.boneyard._dominoes[tiles:]
            yield hand


test_fancy4 = """
    >>> random.seed(42)
    >>> dby1 = FancyDealer4()
    >>> hands = list(dby1.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]

    >>> random.seed(42)
    >>> dby2 = FancyDealer4()
    >>> hands5 = list(dby2.hand_iter(players=2, tiles=5))
    >>> hands5[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6)]
"""


class DominoBoneYard3b:

    hand_size: int = 7

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [Domino(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand3]:
        for p in range(players):
            hand = Hand3(self._dominoes[:self.hand_size])
            self._dominoes = self._dominoes[self.hand_size:]
            yield hand


test_dby5 = """
    >>> random.seed(42)
    >>> dby = DominoBoneYard3b()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hdi = hands[0].highest_double_index()
    >>> hdi
    4
    >>> hands[0][hdi]
    Domino(v1=6, v2=6)
    >>> hands[1]
    [Domino(v1=4, v2=1), Domino(v1=4, v2=4), Domino(v1=3, v2=3), Domino(v1=6, v2=3), Domino(v1=4, v2=2), Domino(v1=5, v2=4), Domino(v1=5, v2=0)]
"""


class DominoBoneYard3c:

    domino_class: Type[Domino] = Domino

    hand_class: Type[Hand] = Hand3

    hand_size: int = 7

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [
            self.domino_class(x, y) for x in range(limit + 1) for y in range(x + 1)
        ]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        for p in range(players):
            hand = self.hand_class(self._dominoes[:self.hand_size])
            self._dominoes = self._dominoes[self.hand_size:]
            yield hand


class Hand4(Hand3):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.doubles = [d for d in self if d.double()]
        self.doubles.sort(key=lambda d: d.score())

    def doubles_indices(self) -> List[int]:
        return [self.index(d) for d in self.doubles]


test_dby6 = """
    >>> random.seed(42)
    >>> dby = DominoBoneYard3c()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hdi = hands[0].highest_double_index()
    >>> hdi
    4
    >>> hands[0][hdi]
    Domino(v1=6, v2=6)
    >>> hands[1]
    [Domino(v1=4, v2=1), Domino(v1=4, v2=4), Domino(v1=3, v2=3), Domino(v1=6, v2=3), Domino(v1=4, v2=2), Domino(v1=5, v2=4), Domino(v1=5, v2=0)]

    >>> random.seed(42)
    >>> DominoBoneYard3c.hand_class = Hand4
    >>> dby = DominoBoneYard3c()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino(v1=5, v2=3), Domino(v1=5, v2=1), Domino(v1=4, v2=0), Domino(v1=6, v2=0), Domino(v1=6, v2=6), Domino(v1=3, v2=0), Domino(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hdi = hands[0].highest_double_index()
    >>> hdi
    4

"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
