#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 15. Example 2.
"""
from typing import (
    NamedTuple,
    List,
    Type,
    Optional,
    Iterator,
    Tuple,
    DefaultDict,
    Union,
    cast,
    Any,
)
import random
from collections import defaultdict

# Duck Typing

from typing import NamedTuple


class Domino_1(NamedTuple):
    v1: int
    v2: int

    @property
    def double(self) -> bool:
        return self.v1 == self.v2

    @property
    def score(self) -> int:
        return self.v1 + self.v2


from dataclasses import dataclass


@dataclass(frozen=True, eq=True, order=True)
class Domino_2:
    v1: int
    v2: int

    @property
    def double(self) -> bool:
        return self.v1 == self.v2

    @property
    def score(self) -> int:
        return self.v1 + self.v2


Domino = Union[Domino_1, Domino_2]


def builder(v1: int, v2: int) -> Domino:
    return Domino_2(v1, v2)


test_dominoe_classes = """
    >>> d_1a = Domino_1(6, 5)
    >>> d_1b = Domino_1(6, 5)
    >>> d_1a == d_1b
    True
    >>> d_1a.double
    False
    >>> d_1a.score
    11

    >>> d_2a = Domino_2(5, 3)
    >>> d_2b = Domino_2(5, 3)
    >>> d_2a == d_2b
    True
    >>> d_2a.double
    False
    >>> d_2a.score
    8
"""

# More Complex Example


class Hand(list):

    def __init__(self, *args: Domino) -> None:
        super().__init__(cast(Tuple[Any], args))

    def score(self) -> int:
        return sum(d.score for d in self)

    def rank(self) -> None:
        self.sort(key=lambda d: d.score, reverse=True)

    def doubles(self) -> List[Domino_1]:
        return [d for d in self if d.double]

    def highest_double(self) -> Optional[Domino_1]:
        descending = sorted(self.doubles(), key=lambda d: d.v1, reverse=True)
        if descending:
            return descending[0]
        return None


class DominoBoneYard:

    domino_class: Type[Domino] = Domino_1

    hand_class: Type[Hand] = Hand

    hand_size: int = 7

    def __init__(self, limit: int = 6) -> None:
        self._dominoes: List[Domino] = [
            self.domino_class(x, y) for x in range(limit + 1) for y in range(x + 1)
        ]
        random.shuffle(self._dominoes)

    def draw(self, n: int = 1) -> Optional[List[Domino]]:
        deal, remainder = self._dominoes[:n], self._dominoes[n:]
        if len(deal) != n:
            return None
        self._dominoes = remainder
        return deal

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        hands: List[Optional[List[Domino]]] = [
            self.draw(self.hand_size) for _ in range(players)
        ]
        if not all(hands):
            raise ValueError(f"Can't deal {self.hand_size} tiles to {players} players")
        yield from (self.hand_class(*h) for h in hands if h is not None)


test_dby = """
    >>> random.seed(42)
    >>> DominoBoneYard.hand_class = Hand
    >>> dby = DominoBoneYard()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [Domino_1(v1=5, v2=3), Domino_1(v1=5, v2=1), Domino_1(v1=4, v2=0), Domino_1(v1=6, v2=0), Domino_1(v1=6, v2=6), Domino_1(v1=3, v2=0), Domino_1(v1=2, v2=2)]
    >>> hands[0].score()
    43
    >>> hd = hands[0].highest_double()
    >>> hd
    Domino_1(v1=6, v2=6)

    >>> hands[1]
    [Domino_1(v1=4, v2=1), Domino_1(v1=4, v2=4), Domino_1(v1=3, v2=3), Domino_1(v1=6, v2=3), Domino_1(v1=4, v2=2), Domino_1(v1=5, v2=4), Domino_1(v1=5, v2=0)]
"""

test_dby_exception = """
    >>> random.seed(42)
    >>> DominoBoneYard.hand_class = Hand
    >>> dby = DominoBoneYard()
    >>> hands = list(dby.hand_iter(5))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/mastering/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_dby_2[3]>", line 1, in <module>
        hands = list(dby.hand_iter(5))
      File "/Users/slott/Documents/.../mastering-oo-python-2e/Chapter_15/ch15_ex2.py", line 119, in hand_iter
        raise ValueError(f"Can't deal {self.hand_size} tiles to {players} players")
    ValueError: Can't deal 7 tiles to 5 players
"""


class Hand_X1(Hand):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.end: DefaultDict[int, List[Domino_1]] = defaultdict(list)
        for d in self:
            self.end[d.v1].append(d)
            self.end[d.v2].append(d)

    def matches(self, spots: int) -> List[Domino_1]:
        return self.end.get(spots, [])


test_dby_3 = """
    >>> random.seed(42)
    >>> DominoBoneYard.hand_class = Hand_X1
    >>> DominoBoneYard.domino_class = Domino_2
    >>> dby = DominoBoneYard()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> h_0 = hands[0]
    >>> h_0
    [Domino_2(v1=5, v2=3), Domino_2(v1=5, v2=1), Domino_2(v1=4, v2=0), Domino_2(v1=6, v2=0), Domino_2(v1=6, v2=6), Domino_2(v1=3, v2=0), Domino_2(v1=2, v2=2)]
    >>> h_0.score()
    43
    >>> h_0.matches(3)
    [Domino_2(v1=5, v2=3), Domino_2(v1=3, v2=0)]
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
