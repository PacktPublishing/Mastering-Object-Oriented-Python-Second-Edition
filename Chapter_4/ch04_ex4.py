#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 4. Example 4.
"""
from typing import Any, Optional

from Chapter_4.ch04_ex1 import Suit


class Card:
    """A poor replacement for polymorphism."""

    def __init__(cls, rank: int, suit: Suit) -> None:
        super().__setattr__("_cache", {"suit": suit, "rank": rank})

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError("Can't Touch That")

    def __getattr__(self, name: str) -> Any:
        if name in self._cache:
            return self._cache[name]
        elif name == "hard":
            if self.rank in (11, 12, 13):
                return 10
            elif self.rank == 1:
                return 1
            elif self.rank in range(2, 10):
                return self.rank
            else:
                raise ValueError("Invalid Rank")
        elif name == "soft":
            if self.rank in (11, 12, 13):
                return 10
            elif self.rank == 1:
                return 11
            elif self.rank in range(2, 10):
                return self.rank
            else:
                raise ValueError("Invalid Rank")
        else:
            raise AttributeError(name)


test_card = """
    >>> c = Card(2, Suit.Club)
    >>> c.rank = 3  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_card[2]>", line 1, in <module>
        c.rank = 3
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex4.py", line 17, in __setattr__
        raise TypeError("Can't Touch That")
    TypeError: Can't Touch That
    >>> c.extra = 3  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_card[2]>", line 1, in <module>
        c.rank = 3
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex4.py", line 17, in __setattr__
        raise TypeError("Can't Touch That")
    TypeError: Can't Touch That
    >>> c.extra  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_card[3]>", line 1, in <module>
        c.extra
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex4.py", line 44, in __getattr__
        raise AttributeError(name)
    AttributeError: extra
    
    >>> c.rank
    2
    >>> c.hard
    2
    >>> c.soft
    2
"""


class RTD_Solver:

    def __init__(
        self, *, rate: float = None, time: float = None, distance: float = None
    ) -> None:
        if rate:
            self.rate = rate
        if time:
            self.time = time
        if distance:
            self.distance = distance

    def __getattr__(self, name: str) -> float:
        if name == "rate":
            print("Computing Rate")
            return self.distance / self.time
        elif name == "time":
            return self.distance / self.rate
        elif name == "distance":
            return self.rate * self.time
        else:
            raise AttributeError(f"Can't compute {name}")


test_rtd = """
    >>> r1 = RTD_Solver(rate=6.25, distance=10.25)
    >>> r1.time
    1.64
    >>> r1.rate
    6.25
"""


class SuperSecret:

    def __init__(self, hidden: Any, exposed: Any) -> None:
        self._hidden = hidden
        self.exposed = exposed

    def __getattribute__(self, item: str):
        if (len(item) >= 2 and item[0] == "_"
                and item[1] != "_"):
            raise AttributeError(item)
        return super().__getattribute__(item)


test_secret = """
    >>> x = SuperSecret('onething', 'another')
    >>> x.exposed
    'another'
    >>> x._hidden  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_secret[3]>", line 1, in <module>
        x._hidden  #
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_4/ch04_ex4.py", line 132, in __getattribute__
        raise AttributeError(item)
    AttributeError: _hidden

    >>> dir(x)  # doctest: +ELLIPSIS
    [..., '_hidden', 'exposed']
    >>> vars(x)
    {'_hidden': 'onething', 'exposed': 'another'}
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
