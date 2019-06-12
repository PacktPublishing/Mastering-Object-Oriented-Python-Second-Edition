#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 4. Example 1.
"""
from enum import Enum
import random
from typing import Any, cast, NamedTuple, Callable, Iterable, Union
from dataclasses import dataclass

# Immutability
# ======================

# Yes, this is out of order from the book.
# It's presented first to make the code below work out nicely.

# A simple-looking card class with comparisons.
# Uses __slots__ to constrain the definition.


class Suit(str, Enum):
    Club = "\N{BLACK CLUB SUIT}"
    Diamond = "\N{BLACK DIAMOND SUIT}"
    Heart = "\N{BLACK HEART SUIT}"
    Spade = "\N{BLACK SPADE SUIT}"


class BlackJackCard:
    """Abstract Superclass."""

    # Note: __slots__ isn't inherited and must be repeated.
    # THe alternative is kind of hideous.
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit!r}, hard={self.hard}, soft={self.soft}"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    # if we don't want to repeat __slots__ we can use this to prevent attributes being set.

    # def __setattr__(self, name: str, value: Any) -> NoReturn:
    #    raise AttributeError(
    #        f"{self.__class__.__name__} has no attribute {name!r}"
    #    )

    def __lt__(self, other: Any) -> bool:
        # Bad idea
        if not issubclass(other.__class__, BlackJackCard):
            return NotImplemented
        return self.rank < cast(BlackJackCard, other).rank

    def __le__(self, other: Any) -> bool:
        # Better idea
        try:
            return self.rank <= cast(BlackJackCard, other).rank
        except AttributeError:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        try:
            return self.rank == cast(BlackJackCard, other).rank and self.suit == cast(
                BlackJackCard, other
            ).suit
        except AttributeError:
            return NotImplemented


class Ace21Card(BlackJackCard):
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank=1, suit={self.suit!r})"


class Face21Card(BlackJackCard):
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)

    def __repr__(self) -> str:
        rank_num = {"J": 11, "Q": 12, "K": 13}[self.rank]
        return f"{self.__class__.__name__}(rank={rank_num}, suit={self.suit!r})"


class Number21Card(BlackJackCard):
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit!r})"


def card21(rank: int, suit: Suit) -> BlackJackCard:
    if rank == 1:
        return Ace21Card(rank, suit)
    elif 2 <= rank < 11:
        return Number21Card(rank, suit)
    elif 11 <= rank < 14:
        return Face21Card(rank, suit)
    else:
        raise TypeError


def compare(a: Any, b: Any) -> None:
    print(f"{a} == {b} {a==b}, {a} < {b} {a<b}, {a} <= {b} {a <= b}")
    print(f"{a} != {b} {a!=b}, {a} > {b} {a>b}, {a} >= {b} {a >= b}")


test_comparisons_21 = """
    >>> c = Ace21Card("A", Suit.Spade)

    >>> c.label = "no slot named label"  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 173, in <module>
        card2d.label = "no slot named label"
    AttributeError: 'Number21Card' object has no attribute 'label'

    >>> print(c.label)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 173, in <module>
        card2d.label = "no slot named label"
    AttributeError: 'Number21Card' object has no attribute 'label'

    >>> c
    Ace21Card(rank=1, suit=<Suit.Spade: '♠'>)
    
    >>> c.rank = 2

    >>> card2d = card21(2, Suit.Diamond)
    >>> card2s = card21(2, Suit.Spade)
    >>> cardkd = card21(13, Suit.Diamond)

    >>> card2d
    Number21Card(rank=2, suit=<Suit.Diamond: '♦'>)

    >>> compare(card2d, card2s)
    2♦ == 2♠ False, 2♦ < 2♠ False, 2♦ <= 2♠ True
    2♦ != 2♠ True, 2♦ > 2♠ False, 2♦ >= 2♠ True
    >>> compare(card2s, cardkd)
    2♠ == K♦ False, 2♠ < K♦ True, 2♠ <= K♦ True
    2♠ != K♦ True, 2♠ > K♦ False, 2♠ >= K♦ False
    >>> compare(card2d, 2)    # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_comparisons_21[10]>", line 1, in <module>
        compare(card2d, 2)    # doctest: +IGNORE_EXCEPTION_DETAIL
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 117, in compare
        print(f"{a} == {b} {a==b}, {a} < {b} {a<b}, {a} <= {b} {a <= b}")
    TypeError: '<' not supported between instances of 'Number21Card' and 'int'
"""


class Deck(list):

    def __init__(
        self, decks: int = 6, factory: Callable[[int, Suit], BlackJackCard] = card21
    ) -> None:
        super().__init__()
        for i in range(decks):
            self.extend(factory(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit))
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


class AceCard2(NamedTuple):
    rank: str
    suit: Suit
    hard: int = 1
    soft: int = 11

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class FaceCard2(NamedTuple):
    rank: str
    suit: Suit
    hard: int = 10
    soft: int = 10

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class NumberCard2(NamedTuple):
    rank: str
    suit: Suit
    hard: int
    soft: int

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


def card2(rank: int, suit: Suit) -> Union[AceCard2, FaceCard2, NumberCard2]:
    """No parent class... """
    if rank == 1:
        return AceCard2("A", suit)
    elif 2 <= rank < 11:
        return NumberCard2(str(rank), suit, rank, rank)
    elif 11 <= rank < 14:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard2(rank_str, suit)
    else:
        raise TypeError


test_comparisons_2 = """
    >>> c = AceCard2("A", Suit.Spade)
    >>> c.rank
    'A'
    >>> c.suit
    <Suit.Spade: '♠'>
    >>> c.hard
    1
    >>> c.not_allowed = 2  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_comparisons_2[3]>", line 1, in <module>
        c.not_allowed = 2
    AttributeError: 'AceCard2' object has no attribute 'not_allowed'
    >>> c.rank = 3  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_comparisons_2[4]>", line 1, in <module>
        c.rank = 3
    AttributeError: can't set attribute

    >>> c.label = "no slot named label"  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 173, in <module>
        card2d.label = "no slot named label"
    AttributeError: 'AceCard2' object has no attribute 'label'

    >>> print(c.label)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 173, in <module>
        card2d.label = "no slot named label"
    AttributeError: 'AceCard2' object has no attribute 'label'

    >>> c
    AceCard2(rank='A', suit=<Suit.Spade: '♠'>, hard=1, soft=11)

    >>> card2d = card2(2, Suit.Diamond)
    >>> card2s = card2(2, Suit.Spade)
    >>> cardkd = card2(13, Suit.Diamond)

    >>> card2d
    NumberCard2(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2)

    >>> compare(card2d, card2s)
    2♦ == 2♠ False, 2♦ < 2♠ False, 2♦ <= 2♠ False
    2♦ != 2♠ True, 2♦ > 2♠ True, 2♦ >= 2♠ True
    >>> compare(card2s, cardkd)
    2♠ == K♦ False, 2♠ < K♦ True, 2♠ <= K♦ True
    2♠ != K♦ True, 2♠ > K♦ False, 2♠ >= K♦ False
    >>> compare(card2d, 2)    # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: '<' not supported between instances of 'NumberCard2' and 'int'
"""


@dataclass(eq=True, order=True, frozen=True)
class AceCard3:
    rank: str
    suit: Suit
    hard: int = 1
    soft: int = 11


@dataclass(eq=True, order=True, frozen=True)
class FaceCard3:
    rank: str
    suit: Suit
    hard: int = 10
    soft: int = 10


@dataclass(eq=True, order=True, frozen=True)
class NumberCard3:
    rank: str
    suit: Suit
    hard: int
    soft: int


def card3(rank, suit) -> Union[AceCard3, FaceCard3, NumberCard3]:
    if rank == 1:
        return AceCard3("A", suit)
    elif 2 <= rank < 11:
        return NumberCard3(str(rank), suit, rank, rank)
    elif 11 <= rank < 14:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard3(rank_str, suit)
    else:
        raise TypeError


test_comparisons_3 = """
    >>> c = AceCard3("A", Suit.Spade)
    
    >>> c.label = "no slot named label"   
    Traceback (most recent call last):
    dataclasses.FrozenInstanceError: cannot assign to field 'label'
    >>> print(c.label)
    Traceback (most recent call last):
    AttributeError: 'AceCard3' object has no attribute 'label'
        
    >>> c
    AceCard3(rank='A', suit=<Suit.Spade: '♠'>, hard=1, soft=11)

    >>> card2d = card3(2, Suit.Diamond)
    >>> card2s = card3(2, Suit.Spade)
    >>> cardkd = card3(13, Suit.Diamond)
    
    >>> card2d
    NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2)

    >>> compare(card2d, card2s)
    NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) == NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) False, NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) < NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) False, NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) <= NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) False
    NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) != NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) True, NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) > NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) True, NumberCard3(rank='2', suit=<Suit.Diamond: '♦'>, hard=2, soft=2) >= NumberCard3(rank='2', suit=<Suit.Spade: '♠'>, hard=2, soft=2) True
    >>> compare(card2s, cardkd)
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_comparisons_3[9]>", line 1, in <module>
        compare(card2s, cardkd)
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex1.py", line 117, in compare
        print(f"{a} == {b} {a==b}, {a} < {b} {a<b}, {a} <= {b} {a <= b}")
    TypeError: '<' not supported between instances of 'NumberCard3' and 'FaceCard3'
    >>> compare(card2d, 2)    # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: '<' not supported between instances of 'NumberCard3' and 'int'
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
