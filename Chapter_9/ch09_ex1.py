#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 9. Example 1.
"""

# Decorator Example 1
# ================================

# Use of builtin decorators

from typing import Any, cast, Optional, Type
from types import TracebackType
import math
import random
from Chapter_6.ch06_ex2 import KnownSequence


class Angle(float):
    __slots__ = ("_degrees",)

    @staticmethod
    def from_radians(value: float) -> "Angle":
        return Angle(180 * value / math.pi)

    def __init__(self, degrees: float) -> None:
        self._degrees = degrees

    @property
    def radians(self) -> float:
        return math.pi * self._degrees / 180

    @property
    def degrees(self) -> float:
        return self._degrees


test_angle = """
    >>> a = Angle(22.5)
    >>> round(a.radians/math.pi, 3)
    0.125
    >>> b = Angle.from_radians(.227)
    >>> round(b.degrees, 1)
    13.0
    >>> b.radians
    0.227
"""

# Decorator Example 2
# ================================

# Use of library decorators.
# Some preliminary definitions

from enum import Enum


class Suit(Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


# Using functools.total_ordering
# Not a good idea. Use dataclasses instead.
import functools


@functools.total_ordering
class CardTO:
    __slots__ = ("rank", "suit")

    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __eq__(self, other: Any) -> bool:
        return self.rank == cast(CardTO, other).rank

    def __lt__(self, other: Any) -> bool:
        return self.rank < cast(CardTO, other).rank

    def __str__(self) -> str:
        return f"{self.rank:d}{self.suit:s}"


test_total_ordering = """
    >>> c1 = CardTO(3, Suit.Clubs)
    >>> c2 = CardTO(3, Suit.Hearts)
    >>> c1 == c2
    True
    >>> c1 < c2
    False
    >>> c1 <= c2
    True
    >>> c1 >= c2
    True
    >>> c1 > c2
    False
    >>> c1 != c2
    False
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CardDC:
    rank: int
    suit: Suit

    def __eq__(self, other: Any) -> bool:
        return self.rank == cast(CardTO, other).rank

    def __lt__(self, other: Any) -> bool:
        return self.rank < cast(CardTO, other).rank

    def __le__(self, other: Any) -> bool:
        return self.rank <= cast(CardTO, other).rank

    def __str__(self) -> str:
        return f"{self.rank:d}{self.suit:s}"


test_dc_ordering = """
    >>> c1 = CardDC(3, Suit.Clubs)
    >>> c2 = CardDC(3, Suit.Hearts)
    >>> c1 == c2
    True
    >>> c1 < c2
    False
    >>> c1 <= c2
    True
    >>> c1 >= c2
    True
    >>> c1 > c2
    False
    >>> c1 != c2
    False
"""

# For later examples


class Deck(list):

    def __init__(self, size: int = 1) -> None:
        for d in range(size):
            cards = [CardDC(r, s) for r in range(1, 14) for s in Suit]
            super().extend(cards)
        random.shuffle(self)


# Mixin example 1
# =======================

# Mixin using enums

from typing import Type, List

from enum import Enum


class EnumDomain:

    @classmethod
    def domain(cls: Type) -> List[str]:
        return [m.value for m in cls]


class SuitD(str, EnumDomain, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


test_enum = """
    >>> SuitD.domain()
    ['♣', '♦', '♥', '♠']
    >>> SuitD.Clubs.center(5)
    '  ♣  '
    
    >>> Suit.Clubs.center(5)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_enum[2]>", line 1, in <module>
        Suit.Clubs.center(5)
    AttributeError: 'Suit' object has no attribute 'center'

    >>> Suit.Clubs.value.center(5)
    '  ♣  '

"""

# Decorator Example 1
# ==============================

# Simple function decorator
import logging, sys
import functools
from typing import Callable, TypeVar, List


FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def debug(function: F) -> F:

    @functools.wraps(function)
    def logged_function(*args, **kw):
        logging.debug("%s(%r, %r)", function.__name__, args, kw)
        result = function(*args, **kw)
        logging.debug("%s = %r", function.__name__, result)
        return result

    return cast(F, logged_function)


@debug
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    else:
        raise Exception(f"Design Error: {vars()}")


test_debug_1 = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    >>> ackermann(2, 4)
    11
    >>> logging.shutdown()
"""

# Decorator Example 2
# ==============================


def debug2(function: F) -> F:
    log = logging.getLogger(function.__name__)

    @functools.wraps(function)
    def logged_function(*args, **kw):
        log.debug("call(%r, %r)", args, kw)
        result = function(*args, **kw)
        log.debug("result = %r", result)
        return result

    return cast(F, logged_function)


@debug2
def ackermann2(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann2(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann2(m - 1, ackermann2(m, n - 1))
    else:
        raise Exception(f"Design Error: {vars()}")


@debug2
def simpler(x: int, y: int) -> int:
    return 2 * x + y


test_debug_2 = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    >>> ackermann2(2, 4)
    11
    >>> simpler(20, 2)
    42
    >>> logging.shutdown()
"""

# Decorator Example 3
# ==============================

# Parameterized decorator
def decorator(config) -> Callable[[F], F]:

    def concrete_decorator(function: F) -> F:

        def wrapped(*args, **kw):
            return function(*args, **kw)

        return cast(F, wrapped)

    return concrete_decorator


def debug_named(log_name: str) -> Callable[[F], F]:
    log = logging.getLogger(log_name)

    def concrete_decorator(function: F) -> F:

        @functools.wraps(function)
        def wrapped(*args, **kw):
            log.debug("%s(%r, %r)", function.__name__, args, kw)
            result = function(*args, **kw)
            log.debug("%s = %r", function.__name__, result)
            return result

        return cast(F, wrapped)

    return concrete_decorator


@debug_named("recursion")
def ackermann3(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann3(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann3(m - 1, ackermann3(m, n - 1))
    else:
        raise Exception(f"Design Error: {vars()}")


test_debug_3 = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    >>> ackermann3(2, 4)
    11
    >>> logging.shutdown()
"""

# Class Decorator 1
# ==============================

# Unit and Standard Unit


def standard(class_: Type) -> Type:
    class_.standard = class_
    return class_


def nonstandard(based_on: Type) -> Callable[[Type], Type]:

    def concrete_decorator(class_: Type) -> Type:
        class_.standard = based_on
        return class_

    return concrete_decorator


class Unit:
    factor = 1.0

    @classmethod
    def value(class_, value: float) -> float:
        if value is None:
            return None
        return value / class_.factor

    @classmethod
    def convert(class_, value: float) -> float:
        if value is None:
            return None
        return value * class_.factor


@standard
class INCH(Unit):
    """inch"""
    name = "in"


@nonstandard(INCH)
class FOOT(Unit):
    """foot"""
    name = "ft"
    factor = 1 / 12


test_class_decorator = """
    >>> length = INCH.value(18)
    >>> print(FOOT.convert(length), FOOT.name, "=", INCH.convert(length), INCH.name)
    1.5 ft = 18.0 in
"""

# Method Decorator
# =============================


def audit(method: F) -> F:

    @functools.wraps(method)
    def wrapper(self, *args, **kw):
        template = "%s\n     before %s\n     after %s"
        audit_log = logging.getLogger("audit")
        before = repr(self)  # a kind of deep copy to preserve state
        try:
            result = method(self, *args, **kw)
        except Exception as e:
            after = repr(self)
            audit_log.exception(template, method.__qualname__, before, after)
            raise
        after = repr(self)
        audit_log.info(template, method.__qualname__, before, after)
        return result

    return cast(F, wrapper)


class Hand:

    def __init__(self, *cards: CardDC) -> None:
        self._cards = list(cards)

    @audit
    def __iadd__(self, card: CardDC) -> "Hand":
        self._cards.append(card)
        self._cards.sort(key=lambda c: c.rank)
        return self

    def __repr__(self) -> str:
        cards = ", ".join(map(str, self._cards))
        return f"{self.__class__.__name__}({cards})"


test_audit = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    >>> with KnownSequence():
    ...     d = Deck()
    ...     h = Hand(d.pop(), d.pop())
    ...     h += d.pop()
    ...     print(h)
    Hand(7Suit.Clubs, 7Suit.Hearts, 13Suit.Clubs)
        
    >>> with KnownSequence():
    ...     d = Deck()
    ...     h = Hand(d.pop(), d.pop())
    ...     h += "Not A Card!"  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_9/ch09_ex1.py", line 390, in wrapper
        result = method(self, *args, **kw)
          File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_9/ch09_ex1.py", line 390, in wrapper
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_9/ch09_ex1.py", line 410, in __iadd__
            result = method(self, *args, **kw)
        self._cards.sort(key=lambda c: c.rank)
          File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_9/ch09_ex1.py", line 410, in __iadd__
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_9/ch09_ex1.py", line 410, in <lambda>
            self._cards.sort(key=lambda c: c.rank)
        self._cards.sort(key=lambda c: c.rank)
    AttributeError: 'str' object has no attribute 'rank'
    
    >>> logging.shutdown()
"""

# More Complex Decoration
# ==================================

# This decorator's effect is effectively hidden from mypy.
# The new method is injected dynamically.


def memento(class_: Type) -> Type:

    def memento_method(self):
        return (
            f"{self.__class__.__qualname__}"
            f"(**{vars(self)!r})"
        )

    class_.memento = memento_method
    return class_


@memento
class StatefulClass:

    def __init__(self, value: Any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"


test_memento_1 = """
    >>> st = StatefulClass(2.7)
    >>> print(st.memento())
    StatefulClass(**{'value': 2.7})
"""


class Memento:

    def memento(self) -> str:
        return f"{self.__class__.__qualname__}(**{vars(self)!r})"


class StatefulClass2(Memento):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


test_memento_2 = """
    >>> st2 = StatefulClass2(2.7)
    >>> print(st2.memento())
    StatefulClass2(**{'value': 2.7})
"""
__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
