#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 3. Example 4.
"""

from typing import Iterable, cast, Any, Union, Type, Tuple
import random
from collections import defaultdict
from Chapter_3.ch03_ex1 import card2, Suit, Card2, AceCard2, FaceCard2, NumberCard2
from Chapter_3.ch03_ex3 import Hand, FrozenHand


class Deck(list):

    def __init__(self) -> None:
        super().__init__(
            card2(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit)
        )
        random.shuffle(self)

# __hash__
# =========

test_hash = """
    >>> v1 = 123_456_789
    >>> v2 = 2_305_843_009_337_150_740
    >>> hash(v1)
    123456789
    >>> hash(v2)
    123456789
    >>> v2 == v1
    False
"""

# __bool__
# ====================

# Not much to show here. The default works as expected.

# __format__
# =====================
#
# Really, this belongs with __str__() and __repr__()
#

# Examples of how __format__ gets invoked

test_format = """
    >>> c = card2(2, Suit.Club)
    >>> print("function", format(c))
    function 2♣
    >>> print(f"Card plain {c}")
    Card plain 2♣
    >>> print(f"Card !r {c!r}")
    Card !r NumberCard2(suit=<Suit.Club: '♣'>, rank='2')
    >>> print(f"Card !s {c!s}")
    Card !s 2♣

    # Our own unique formatting language uses "r" and "s" for rank and suit.

    >>> print("Card :%s {0:%s}".format(c))
    Card :%s ♣
    >>> print("Card :%r {0:%r}".format(c))
    Card :%r 2
    >>> print("Card :%r of %s {0:%r of %s}".format(c))
    Card :%r of %s 2 of ♣
    >>> print("Card :%s%r {0:%s%r}".format(c))
    Card :%s%r ♣2

    # Extra literals we leave alone.

    >>> print("Card nested {0:{fill}{align}16s}".format(c, fill="*", align="<"))
    Card nested *<16s
"""

# RE to parse the specification.

import re

spec_pat = re.compile(
    r"(?P<fill_align>.?[\<\>=\^])?"
    "(?P<sign>[-+ ])?"
    "(?P<alt>#)?"
    "(?P<padding>0)?"
    "(?P<width>\d*)"
    "(?P<comma>,)?"
    "(?P<precision>\.\d*)?"
    "(?P<type>[bcdeEfFgGnosxX%])?"
)

test_spec_pat = """
    >>> for spec in (
    ...     "<30",
    ...     ">30",
    ...     "^30",
    ...     "*^30",
    ...     "+f",
    ...     "-f",
    ...     " f",
    ...     "d",
    ...     "x",
    ...     "o",
    ...     "b",
    ...     "#x",
    ...     "#o",
    ...     "#b",
    ...     ",",
    ...     ".2%",
    ...     "06.4f",
    ... ):
    ...     print(spec, spec_pat.match(spec).groupdict())
    <30 {'fill_align': '<', 'sign': None, 'alt': None, 'padding': None, 'width': '30', 'comma': None, 'precision': None, 'type': None}
    >30 {'fill_align': '>', 'sign': None, 'alt': None, 'padding': None, 'width': '30', 'comma': None, 'precision': None, 'type': None}
    ^30 {'fill_align': '^', 'sign': None, 'alt': None, 'padding': None, 'width': '30', 'comma': None, 'precision': None, 'type': None}
    *^30 {'fill_align': '*^', 'sign': None, 'alt': None, 'padding': None, 'width': '30', 'comma': None, 'precision': None, 'type': None}
    +f {'fill_align': None, 'sign': '+', 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'f'}
    -f {'fill_align': None, 'sign': '-', 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'f'}
     f {'fill_align': None, 'sign': ' ', 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'f'}
    d {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'd'}
    x {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'x'}
    o {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'o'}
    b {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'b'}
    #x {'fill_align': None, 'sign': None, 'alt': '#', 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'x'}
    #o {'fill_align': None, 'sign': None, 'alt': '#', 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'o'}
    #b {'fill_align': None, 'sign': None, 'alt': '#', 'padding': None, 'width': '', 'comma': None, 'precision': None, 'type': 'b'}
    , {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': ',', 'precision': None, 'type': None}
    .2% {'fill_align': None, 'sign': None, 'alt': None, 'padding': None, 'width': '', 'comma': None, 'precision': '.2', 'type': '%'}
    06.4f {'fill_align': None, 'sign': None, 'alt': None, 'padding': '0', 'width': '6', 'comma': None, 'precision': '.4', 'type': 'f'}
"""

# Nested {}'s

test_nested_curlies = """
    >>> random.seed(9973)
    >>> stats = defaultdict(int)
    >>> d = Deck()
    >>> h1 = FrozenHand(d.pop(), d.pop(), d.pop())
    >>> stats[h1] += 1
    >>> h2 = FrozenHand(d.pop(), d.pop(), d.pop())
    >>> stats[h2] += 1

    >>> width = 6
    >>> for hand, count in stats.items():
    ...     print("{hand:%r%s} {count:{width}d}".format(hand=hand, count=count, width=width))
    5♦, 5♠      1
    8♠, 9♦      1
"""

# __bytes__
# =====================
#

# Export Card2 instance as a bytes. Recover a Card2 instance from bytes.


def card_from_bytes(buffer: bytes) -> Card2:
    """Parses bytes to rebuild the original Card2 instance."""
    string = buffer.decode("utf8")
    try:
        if not (string[0] == "(" and string[-1] == ")"):
            raise ValueError
        code, rank_number, suit_value = string[1:-1].split()
        if int(rank_number) not in range(1, 14):
            raise ValueError
        class_ = {"A": AceCard2, "N": NumberCard2, "F": FaceCard2}[code]
        return class_(int(rank_number), Suit(suit_value))
    except (IndexError, KeyError, ValueError) as ex:
        raise ValueError(f"{buffer!r} isn't a Card2 instance")


test_bytes = """
    >>> random.seed(1138)
    >>> d = Deck()
    >>> c = d.pop()
    >>> c
    NumberCard2(suit=<Suit.Heart: '♥'>, rank='5')
    >>> b = bytes(c)
    >>> print(b)
    b'(N 5 \\xe2\\x99\\xa5)'

    >>> data = b'(N 5 \\xe2\\x99\\xa5)'
    >>> c2 = card_from_bytes(data)
    >>> c2
    NumberCard2(suit=<Suit.Heart: '♥'>, rank='5')
    
    >>> card_from_bytes(b'random')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: b'random' isn't a Card2 instance
    >>> card_from_bytes(b'(less random)')
    Traceback (most recent call last):
    ValueError: b'(less random)' isn't a Card2 instance
    >>> card_from_bytes(b'(X 5 \\xe2\\x99\\xa5)')
    Traceback (most recent call last):
    ValueError: b'(X 5 \\xe2\\x99\\xa5)' isn't a Card2 instance
    >>> card_from_bytes(b'(N 25 \\xe2\\x99\\xa5)')
    Traceback (most recent call last):
    ValueError: b'(N 25 \\xe2\\x99\\xa5)' isn't a Card2 instance
    >>> card_from_bytes(b'(N 5 nope)')
    Traceback (most recent call last):
    ValueError: b'(N 5 nope)' isn't a Card2 instance
"""

# Comparison
# ====================

# The object resolution for comparison special methods.
# A partial class to see what happens.


class BlackJackCard_p:

    def __init__(self, rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __lt__(self, other: Any) -> bool:
        print(f"Compare {self} < {other}")
        return self.rank < cast(BlackJackCard_p, other).rank

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


test_blackjackcard_partial = """
    >>> two = BlackJackCard_p(2, Suit.Spade)
    >>> three = BlackJackCard_p(3, Suit.Spade)
    >>> two < three
    Compare 2♠ < 3♠
    True
    >>> two > three
    Compare 3♠ < 2♠
    False
    >>> two == three
    False
    
    >>> two <= three  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_blackjackcard_partial[5]>", line 1, in <module>
        print("{0} <= {1} :: {2!r}".format(two, three, two <= three))  # doctest: +IGNORE_EXCEPTION_DETAIL
    TypeError: '<=' not supported between instances of 'BlackJackCard_p' and 'BlackJackCard_p'
    
    >>> two_c = BlackJackCard_p(2, Suit.Club)
    >>> two_c == BlackJackCard_p(2, Suit.Club)
    False
"""

# A more complete class to show same-class comparisons.


class BlackJackCard:

    def __init__(self, rank: int, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented
        return self.rank < other.rank

    def __le__(self, other: Any) -> bool:
        try:
            return self.rank <= cast(BlackJackCard, other).rank
        except AttributeError:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented
        return self.rank > other.rank

    def __ge__(self, other: Any) -> bool:
        try:
            return self.rank >= cast(BlackJackCard, other).rank
        except AttributeError:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented
        return (self.rank == other.rank
                and self.suit == other.suit)

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, BlackJackCard):
            return NotImplemented
        return (self.rank != other.rank
                or self.suit != other.suit)

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"(rank={self.rank!r}, suit={self.suit!r}, "
                f"hard={self.hard!r}, soft={self.soft!r})")


class Ace21Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)

    def __str__(self) -> str:
        return f"A{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r}, hard={self.hard!r}, soft={self.soft!r})"


class Face21Card(BlackJackCard):

    FACE_MAP = {11: "J", 12: "Q", 13: "K"}

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)

    def __str__(self) -> str:
        return f"{self.FACE_MAP[self.rank]}{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank!r}, suit={self.suit!r}, hard={self.hard!r}, soft={self.soft!r})"


class Number21Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, rank, rank)


def card21(rank: int, suit: Suit) -> BlackJackCard:
    if rank == 1:
        return Ace21Card(rank, suit)
    elif 2 <= rank < 11:
        return Number21Card(rank, suit)
    elif 11 <= rank < 14:
        return Face21Card(rank, suit)
    else:
        raise TypeError


test_blackjack_full = """
    >>> two = card21(2, "♠")
    >>> three = card21(3, "♠")
    >>> f"{two} <  {three} is {two < three}"
    '2♠ <  3♠ is True'
    >>> f"{two} >  {three} is {two > three}"
    '2♠ >  3♠ is False'
    >>> f"{two} == {three} is {two == three}"
    '2♠ == 3♠ is False'
    >>> f"{two} <= {three} is {two <= three}"
    '2♠ <= 3♠ is True'

    >>> two_c = card21(2, "♣")
    >>> f"{two} == {two_c} is {two == two_c}"
    '2♠ == 2♣ is False'
    >>> two.rank == two_c.rank
    True
 
    >>> # A mixed class comparison with int
    >>> f"2 <  {three} is {2 < three}"  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_blackjack_full[8]>", line 1, in <module>
        print("{0} <  {1} :: {2!r}".format(2, three, 2 < three))  # doctest: +IGNORE_EXCEPTION_DETAIL
    TypeError: '<' not supported between instances of 'int' and 'Number21Card'
    >>> two < 2  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_blackjack_full[10]>", line 1, in <module>
        two < 2
    TypeError: '<' not supported between instances of 'Number21Card' and 'int'
    >>> two > 2  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_blackjack_full[11]>", line 1, in <module>
        two > 2
    TypeError: '>' not supported between instances of 'Number21Card' and 'int'
    >>> two == 2
    False
    >>> 2 == two
    False
"""

test_hand = """
    >>> two = card21(2, Suit.Spade) 
    >>> three = card21(3, Suit.Spade) 
    >>> two_c = card21(2, Suit.Club) 
    >>> ace = card21(1, Suit.Club) 
    >>> cards = [ace, two, two_c, three] 

    >>> h = Hand( card21(10,'♠'), *cards ) 
    >>> print(h) 
    A♣, 2♠, 2♣, 3♠
    >>> h.total()
    18

"""


# Destruction and __del__()
# ====================================

# Noisy Exit


class Noisy:

    def __del__(self) -> None:
        print(f"Removing {id(self)}")


# Simple create and delete.

test_noisy_1 = """
    >>> x = Noisy()
    >>> del x  # doctest: +ELLIPSIS
    Removing ...
"""

# Shallow copy and multiple references.


test_noisy_2 = """
    >>> ln = [Noisy(), Noisy()]
    >>> ln2 = ln[:]
    >>> del ln  # doctest: +ELLIPSIS
    >>> del ln2  # doctest: +ELLIPSIS
    Removing ...
    Removing ...
"""

# Circularity


class Parent:

    def __init__(self, *children: 'Child') -> None:
        for child in children:
            child.parent = self
        self.children = {c.id: c for c in children}

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )


class Child:

    def __init__(self, id: str) -> None:
        self.id = id
        self.parent: Parent = cast(Parent, None)

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )


test_circularity_fail = """
    >>> p = Parent(Child('a'), Child('b'))
    >>> del p  # doctest: +ELLIPSIS
    
    >>> p_0 = Parent()
    >>> del p_0  # doctest: +ELLIPSIS
    Removing Parent ...

    >>> import gc
    >>> gc.collect()  # doctest: +ELLIPSIS
    Removing Child ...
    Removing Child ...
    Removing Parent ...
    ...

    >>> print(gc.garbage)
    []
"""

# No circularity via weak references.


from weakref import ref


class Parent2:

    def __init__(self, *children: 'Child2') -> None:
        for child in children:
            child.parent = ref(self)
        self.children = {c.id: c for c in children}

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )

class Child2:

    def __init__(self, id: str) -> None:
        self.id = id
        self.parent: ref[Parent2] = cast(ref[Parent2], None)

    def __del__(self) -> None:
        print(
            f"Removing {self.__class__.__name__} {id(self):d}"
        )


test_circularity_pass = """
    >>> p = Parent2(Child('a'), Child('b'))
    >>> del p    # doctest: +ELLIPSIS
    Removing Parent2 ...
    Removing Child ...
    Removing Child ...
"""

# Immutable init and __new__()
# ========================================

# Doesn't work. Can't use this form of __init__ with immutable classes.

class Float_Fail(float):

    def __init__(self, value: float, unit: str) -> None:
        super().__init__(value)
        self.unit = unit


test_float_fail = """
    >>> x = Float_Fail(6.8, "knots")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_float_fail[0]>", line 1, in <module>
        x = Float_Fail(6.8, "knots")
    TypeError: float expected at most 1 arguments, got 2
"""


# This is how we can tweak an immutable object before the __init__ is invoked.

# See https://github.com/python/mypy/issues/1053
# This *should* work since v0.3.1

# Adding type hints will report mypy errors.
# float is (implicitly) a subclass of object.
# object.__new__() takes no arguments.
# float.__new__() is *really* more like type.__new__

class Float_Units(float):

    def __new__(cls, value, unit):
        obj = super().__new__(cls, float(value))
        obj.unit = unit
        return obj

from typing import overload, Optional, SupportsFloat

class Float_Units_Ugly(float):

    unit: str

    def __new__(cls: Type, value: SupportsFloat, unit: str) -> 'Float_Units_Ugly':
        obj = cast('Float_Units_Ugly', cast(type, super()).__new__(cls, float(value)))
        obj.unit = unit
        return obj


test_float_pass = """
    >>> speed = Float_Units(6.8, "knots")
    >>> speed*2
    13.6
    >>> speed.unit
    'knots'
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
