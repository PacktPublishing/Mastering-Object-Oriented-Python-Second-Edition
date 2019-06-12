#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 7. Example 2.
"""
from typing import List, cast, Any, Optional, Iterable, overload, Union, Iterator

# Extending Classes
# ##############################

# Basic Stats formulae
import math


def mean(outcomes: List[float]) -> float:
    return sum(outcomes) / len(outcomes)


def stdev(outcomes: List[float]) -> float:
    n = float(len(outcomes))
    return math.sqrt(n * sum(x ** 2 for x in outcomes) - sum(outcomes) ** 2) / n


test_stats = """
    >>> sample_data = [2, 4, 4, 4, 5, 5, 7, 9]
    >>> mean(sample_data)
    5.0
    >>> stdev(sample_data)
    2.0
"""


# A simple (lazy) stats list class.
# Note the difficulty in expressing a type constraint: List[float].


class StatsList(list):

    def __init__(self, iterable: Optional[Iterable[float]]) -> None:
        super().__init__(cast(Iterable[Any], iterable))

    @property
    def mean(self) -> float:
        return sum(self) / len(self)

    @property
    def stdev(self) -> float:
        n = len(self)
        return math.sqrt(n * sum(x ** 2 for x in self) - sum(self) ** 2) / n


test_lazy_stats_list = """
    >>> sl = StatsList([2, 4, 4, 4, 5, 5, 7, 9])
    >>> sl.mean
    5.0
    >>> sl.stdev
    2.0
    >>> sl[2] = 10
    >>> round(sl.mean, 2)
    5.75
    >>> round(sl.stdev, 2)
    2.54
"""

import random


def data_gen() -> int:
    return random.randint(1, 6) + random.randint(1, 6)


def demo_statslist() -> None:
    """
    >>> random.seed(42)
    >>> demo_statslist()
    mean = 7.000000
    stdev= 2.328
    """
    random.seed(42)
    data = [data_gen() for _ in range(100)]
    stats = StatsList(data)
    print(f"mean = {stats.mean:f}")
    print(f"stdev= {stats.stdev:.3f}")


class Explore(list):

    # There are two overloaded definitions, the type hints tend to be complex for this case
    def __getitem__(self, index):
        print(index, index.indices(len(self)))
        return super().__getitem__(index)


test_explore = """
>>> x= Explore('abcdefg')
>>> x[:]
slice(None, None, None) (0, 7, 1)
['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> x[:-1]
slice(None, -1, None) (0, 6, 1)
['a', 'b', 'c', 'd', 'e', 'f']
>>> x[1:]
slice(1, None, None) (1, 7, 1)
['b', 'c', 'd', 'e', 'f', 'g']
>>> x[::2]
slice(None, None, 2) (0, 7, 2)
['a', 'c', 'e', 'g']
"""

# Eager Stats List class
# Note the difficulty in expressing a type constraint: List[float].


class StatsList2(list):
    """Eager Stats."""

    def __init__(self, iterable: Optional[Iterable[float]]) -> None:
        self.sum0 = 0  # len(self), sometimes called "N"
        self.sum1 = 0.0  # sum(self)
        self.sum2 = 0.0  # sum(x**2 for x in self)
        super().__init__(cast(Iterable[Any], iterable))
        for x in self:
            self._new(x)

    def _new(self, value: float) -> None:
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    def _rmv(self, value: float) -> None:
        self.sum0 -= 1
        self.sum1 -= value
        self.sum2 -= value * value

    def insert(self, index: int, value: float) -> None:
        super().insert(index, value)
        self._new(value)

    def pop(self, index: int = 0) -> None:
        value = super().pop(index)
        self._rmv(value)
        return value

    def append(self, value: float) -> None:
        super().append(value)
        self._new(value)

    def extend(self, sequence: Iterable[float]) -> None:
        super().extend(sequence)
        for value in sequence:
            self._new(value)

    def remove(self, value: float) -> None:
        super().remove(value)
        self._rmv(value)

    def __iadd__(self, sequence: Iterable[float]) -> "StatsList2":
        for v in sequence:
            self.append(v)
        return self

    def __add__(self, sequence: Iterable[float]) -> "StatsList2":
        generic = super().__add__(cast(StatsList2, sequence))
        result = StatsList2(generic)
        return result

    # reveal_type(list.__iadd__)
    # reveal_type(list.__add__)
    # reveal_type(StatsList2.__iadd__)
    # reveal_type(StatsList2.__add__)

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(self.sum0 * self.sum2 - self.sum1 * self.sum1) / self.sum0

    @overload
    def __setitem__(self, index: int, value: float) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[float]) -> None:
        ...

    def __setitem__(self, index, value) -> None:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__setitem__(index, value)
            for x in olds:
                self._rmv(x)
            for x in value:
                self._new(x)
        else:
            old = self[index]
            super().__setitem__(index, value)
            self._rmv(old)
            self._new(value)

    def __delitem__(self, index: Union[int, slice]) -> None:
        # Index may be a single integer, or a slice
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__delitem__(index)
            for x in olds:
                self._rmv(x)
        else:
            old = self[index]
            super().__delitem__(index)
            self._rmv(old)

    # reveal_type(list.__setitem__)
    # reveal_type(MutableSequence.__setitem__)
    # reveal_type(StatsList2.__setitem__)

    # reveal_type(list.__delitem__)
    # reveal_type(StatsList2.__delitem__)


test_eager_stats_list = """
    >>> sl2 = StatsList2([2, 4, 3, 4, 5, 5, 7, 9, 10])
    >>> print("start", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    start [2, 4, 3, 4, 5, 5, 7, 9, 10] 9 49.0 325.0

    >>> sl2[2] = 4
    >>> print("replace", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    replace [2, 4, 4, 4, 5, 5, 7, 9, 10] 9 50.0 332.0

    >>> del sl2[-1]
    >>> print("remove", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    remove [2, 4, 4, 4, 5, 5, 7, 9] 8 40.0 232.0

    >>> sl2.insert(0, -1)
    >>> print("insert", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    insert [-1, 2, 4, 4, 4, 5, 5, 7, 9] 9 39.0 233.0
    
    >>> r = sl2.pop()
    >>> print("pop", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    pop [2, 4, 4, 4, 5, 5, 7, 9] 8 40.0 232.0

    >>> sl2.append(1)
    >>> print("append", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    append [2, 4, 4, 4, 5, 5, 7, 9, 1] 9 41.0 233.0
    
    >>> sl2.extend([10, 11, 12])
    >>> print("extend", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    extend [2, 4, 4, 4, 5, 5, 7, 9, 1, 10, 11, 12] 12 74.0 598.0
    
    >>> sl2.remove(-2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_eager_stats_list[14]>", line 1, in <module>
        sl2.remove(-2)  # doctest: +IGNORE_EXCEPTION_DETAIL
      File "/Users/slott/Documents/Writing/Python/Mastering OO Python 2e/mastering-oo-python-2e/Chapter_7/ch07_ex1.py", line 438, in remove
        super().remove(value)
    ValueError: list.remove(x): x not in list

    >>> print("failed remove", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    failed remove [2, 4, 4, 4, 5, 5, 7, 9, 1, 10, 11, 12] 12 74.0 598.0
    
    >>> sl2 += [21, 22, 23]
    >>> print("+=", sl2, sl2.sum0, sl2.sum1, sl2.sum2)
    += [2, 4, 4, 4, 5, 5, 7, 9, 1, 10, 11, 12, 21, 22, 23] 15 140.0 2052.0

    >>> sl = StatsList([2, 4, 4, 4, 5, 5, 7, 9, 1, 10, 11, 12, 21, 22, 23])
    >>> print("expected", len(sl), "actual", sl2.sum0)
    expected 15 actual 15
    >>> print("expected", sum(sl), "actual", sl2.sum1)
    expected 140 actual 140.0
    >>> print("expected", sum(x * x for x in sl), "actual", sl2.sum2)
    expected 2052 actual 2052.0
    >>> sl.mean == sl2.mean
    True
    >>> sl.stdev == sl2.stdev
    True

    >>> sl2a = StatsList2([2, 4, 3, 4, 5, 5, 7, 9, 10])
    >>> del sl2a[1:3]
    >>> print('slice del', sl2a, sl2a.sum0, sl2a.sum1, sl2a.sum2)
    slice del [2, 4, 5, 5, 7, 9, 10] 7 42.0 300.0
"""

# Wrapping Classes
# ##############################

# Stats List Wrapper
class StatsList3:

    def __init__(self) -> None:
        self._list: List[float] = list()
        self.sum0 = 0  # len(self), sometimes called "N"
        self.sum1 = 0.  # sum(self)
        self.sum2 = 0.  # sum(x**2 for x in self)

    def append(self, value: float) -> None:
        self._list.append(value)
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    # etc.

    def __getitem__(self, index: int) -> float:
        return self._list.__getitem__(index)

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(self.sum0 * self.sum2 - self.sum1 * self.sum1) / self.sum0


test_wrapper_stats_list = """
    >>> sl3 = StatsList3()
    >>> for data in 2, 4, 4, 4, 5, 5, 7, 9:
    ...    sl3.append(data)
    >>> print(f"Mean {sl3.mean:.1f}, Standard Deviation {sl3.stdev:.1f}")
    Mean 5.0, Standard Deviation 2.0
"""

# Heading 4 -- Extending Classes
# ##############################


# Stats Counter
import math
from collections import Counter


class StatsCounter(Counter):

    @property
    def mean(self) -> float:
        sum0 = sum(v for k, v in self.items())
        sum1 = sum(k * v for k, v in self.items())
        return sum1 / sum0

    @property
    def stdev(self) -> float:
        sum0 = sum(v for k, v in self.items())
        sum1 = sum(k * v for k, v in self.items())
        sum2 = sum(k * k * v for k, v in self.items())
        return math.sqrt(sum0 * sum2 - sum1 * sum1) / sum0

    @property
    def median(self) -> Any:
        all = list(sorted(self.elements()))
        return all[len(all) // 2]

    @property
    def median2(self) -> Optional[float]:
        mid = sum(self.values()) // 2
        low = 0
        for k, v in sorted(self.items()):
            if low <= mid < low + v:
                return k
            low += v
        return None


test_stats_counter = """
    >>> sc = StatsCounter([2, 4, 4, 4, 5, 5, 7, 9])
    >>> print(sc.mean, sc.stdev, sc.most_common(), sc.median, sc.median2)
    5.0 2.0 [(4, 3), (5, 2), (2, 1), (7, 1), (9, 1)] 5 5
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    # performance()
