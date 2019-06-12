#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 6. Example 1.
"""
from typing import Callable, Dict

# Callable
# ======================

# Callable Example #1. Inefficient.  But. It does work.

IntExp = Callable[[int, int], int]

class Power1:

    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x
        return p

pow1: IntExp = Power1()

test_power1 = """
    >>> pow1 = Power1()
    >>> pow1(2, 1024)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216
"""

# Example 2. Subtle error, can be detected by the class definition
# Disliked by mypy as an 'Invalid base class' error: we're forced to ignore it.
from collections.abc import Callable as CallableClass
class Power2(CallableClass):  # type: ignore

    def __call_(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x
        return p

test_power2 = """
    >>> pow2 = Power2()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_power2[0]>", line 1, in <module>
        pow2 = Power2()
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/typing.py", line 813, in __new__
        obj = super().__new__(cls, *args, **kwds)
    TypeError: Can't instantiate abstract class Power2 with abstract methods __call__
"""

# Example 3. Subtle error, detectable by mypy.
class Power3:

    def __call_(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x
        return p

# mypy will detect this problem.
# Chapter_6/ch06_ex1.py:68: error: Incompatible types in assignment (expression has type "Power3", variable has type "Callable[[int, int], int]")
pow3: IntExp = Power3()

test_power3 = """
    >>> pow3 = Power3()
    >>> pow3(2, 1024)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_power3[1]>", line 1, in <module>
        pow3(2, 1024)
    TypeError: 'Power3' object is not callable
"""

class Power4:

    def __call__(self, x: int, n: int) -> int:
        if n == 0:
            return 1
        elif n % 2 == 1:
            return self.__call__(x, n - 1) * x
        else:  # n % 2 == 0:
            t = self.__call__(x, n // 2)
            return t * t

pow4: IntExp = Power4()

test_power4 = """
    >>> pow4(2, 1024)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216
"""


# Example 4, iterative, also super efficient.


class Power4i:

    def __call__(self, x: int, n: int) -> int:
        p = 1
        while n != 0:
            if n % 2 == 1:
                p *= x
                n -= 1
            else:  # n % 2 == 0:
                t = self.__call__(x, n // 2)
                p *= t
                p *= t
                n = 0
        return p

pow4i: IntExp = Power4i()

test_power4i = """
    >>> pow4i(2, 1024)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216
"""

# Example 5, memoization


class Power5:

    def __init__(self) -> None:
        self.memo: Dict[int, int] = {}

    def __call__(self, x: int, n: int) -> int:
        if (x, n) not in self.memo:
            if n == 0:
                self.memo[x, n] = 1
            elif n % 2 == 1:
                self.memo[x, n] = self.__call__(x, n - 1) * x
            elif n % 2 == 0:
                t = self.__call__(x, n // 2)
                self.memo[x, n] = t * t
            else:
                raise Exception("Logic Error")
        return self.memo[x, n]

pow5: IntExp = Power5()

test_power5 = """
    >>> pow5(2, 1024)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216
"""

# Example 6, functools memoization
from functools import lru_cache

@lru_cache()
def pow6(x: int, n: int) -> int:
    if n == 0:
        return 1
    elif n % 2 == 1:
        return pow6(x, n - 1) * x
    else:  # n % 2 == 0:
        t = pow6(x, n // 2)
        return t * t

test_power6 = """
    >>> pow6(2, 1024)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216
"""


def performance() -> None:
    """Timeit results"""
    import timeit

    iterative = timeit.timeit(
        "pow1(2, 1024)",
        """
class Power1:
    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x
        return p

pow1= Power1()
    """,
        number=100_000,
    )  # otherwise it takes 2 minutes
    print("Iterative", iterative)

    recursive = timeit.timeit(
        "pow4(2,1024)",
        """
class Power4:
    def __call__(self, x: int, n: int) -> int:
        if n == 0: return 1
        elif n % 2 == 1: return self.__call__(x, n-1) * x
        else: # n % 2 == 0:
            t= self.__call__(x, n//2)
            return t*t

pow4= Power4()
    """,
        number=100_000,
    )
    print("Recursive", recursive)

    memoized = timeit.timeit(
        "pow5(2,1024)",
        """
class Power5:
    def __init__( self ) -> None:
        self.memo = {}
    def __call__(self, x: int, n: int) -> int:
        if (x,n) not in self.memo:
            if n == 0:
                self.memo[x,n]= 1
            elif n % 2 == 1:
                self.memo[x,n]= self.__call__(x, n-1) * x
            elif n % 2 == 0:
                t= self.__call__(x, n//2)
                self.memo[x,n]= t*t
            else:
                raise Exception("Logic Error")
        return self.memo[x,n]

pow5 = Power5()
    """,
        number=100_000,
    )
    print("Memoized", memoized)


# Some additional Callable Examples
# ---------------------------------

# The BetingStrategy superclass.
class BettingStrategy:

    def __init__(self) -> None:
        self._win = 0
        self._loss = 0

    @property
    def win(self) -> int:
        return self._win

    @win.setter
    def win(self, value: int) -> None:
        self._win = value
        self.stage = 1

    @property
    def loss(self) -> int:
        return self._loss

    @loss.setter
    def loss(self, value: int) -> None:
        self._loss = value

    def __call__(self) -> int:
        return 1

test_flat_betting_strategy = """
    >>> bet = BettingStrategy()
    >>> bet()
    1
    >>> bet.win += 1
    >>> bet()
    1
    >>> bet.loss += 1
    >>> bet()
    1
"""

# A stateful betting strategy. Property-based
class BettingMartingale(BettingStrategy):

    def __init__(self) -> None:
        self._win = 0
        self._loss = 0
        self.stage = 1

    @property
    def win(self) -> int:
        return self._win

    @win.setter
    def win(self, value: int) -> None:
        self._win = value
        self.stage = 1

    @property
    def loss(self) -> int:
        return self._loss

    @loss.setter
    def loss(self, value: int) -> None:
        self._loss = value
        self.stage *= 2

    def __call__(self) -> int:
        return self.stage

test_martingale_betting_strategy = """
    >>> bet = BettingMartingale()
    >>> bet()
    1
    >>> bet.win += 1
    >>> bet()
    1
    >>> bet.loss += 1
    >>> bet()
    2
    >>> bet.loss += 1
    >>> bet()
    4
    >>> bet.win += 1
    >>> bet()
    1
"""

# Another stateful betting strategy, using ``__setattr__()`` instead
# if properties.
class BettingMartingale2(BettingStrategy):

    def __init__(self) -> None:
        self.win = 0
        self.loss = 0
        self.stage = 1

    def __setattr__(self, name: str, value: int) -> None:
        if name == "win":
            self.stage = 1
        elif name == "loss":
            self.stage *= 2
        super().__setattr__(name, value)

    def __call__(self) -> int:
        return self.stage

test_martingale2_betting_strategy = """
    >>> bet = BettingMartingale2()
    >>> bet()
    1
    >>> bet.win += 1
    >>> bet()
    1
    >>> bet.loss += 1
    >>> bet()
    2
    >>> bet.loss += 1
    >>> bet()
    4
    >>> bet.win += 1
    >>> bet()
    1
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)

    # Takes 12 seconds.
    # performance()