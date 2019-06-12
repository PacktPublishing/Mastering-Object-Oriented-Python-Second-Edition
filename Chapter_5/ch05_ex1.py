#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 5. Example 1.
"""
from typing import Any, Union

# Metaclass
# ======================

# Abstract Base Class Example.

from abc import ABCMeta, abstractmethod, ABC

class Card:
    pass


class Hand(list):
    def __init__(self, *cards: Card) -> None:
        super().__init__(cards)


class AbstractBettingStrategy(metaclass=ABCMeta):

    @abstractmethod
    def bet(self, hand: Hand) -> int:
        return 1

    @abstractmethod
    def record_win(self, hand: Hand) -> None:
        pass

    @abstractmethod
    def record_loss(self, hand: Hand) -> None:
        pass

class AbstractBettingStrategy2(ABC):

    @abstractmethod
    def bet(self, hand: Hand) -> int:
        return 1

    @abstractmethod
    def record_win(self, hand: Hand) -> None:
        pass

    @abstractmethod
    def record_loss(self, hand: Hand) -> None:
        pass

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        """Validate the class definition is complete."""
        if cls is AbstractBettingStrategy2:
            has_bet = any(hasattr(B, "bet") for B in subclass.__mro__)
            has_record_win =  any(hasattr(B, "record_win") for B in subclass.__mro__)
            has_record_loss = any(hasattr(B, "record_loss") for B in subclass.__mro__)
            if has_bet and has_record_win and has_record_loss:
                return True
        # print(f"has_bet {has_bet}, has_record_win {has_record_win}, has_record_loss {has_record_loss}")
        return False

test_broken = """
    >>> class Simple_Broken(AbstractBettingStrategy):
    ...     def bet(self, hand: Hand) -> int:
    ...         return 1
    >>> simple = Simple_Broken()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_broken[0]>", line 1, in <module>
        simple = Simple_Broken()  # doctest: +IGNORE_EXCEPTION_DETAIL
    TypeError: Can't instantiate abstract class Simple_Broken with abstract methods record_loss, record_win
"""


test_broken_2 = """
    >>> class Simple_Broken2(AbstractBettingStrategy2):
    ...     def bet(self, hand: Hand) -> int:
    ...         return 1
    ...
    >>> simple2 = Simple_Broken2()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_broken_2[1]>", line 1, in <module>
        simple2 = Simple_Broken2()
    TypeError: Can't instantiate abstract class Simple_Broken2 with abstract methods record_loss, record_win     
"""


class Simple(AbstractBettingStrategy):

    def bet(self, hand: Hand) -> int:
        return 1

    def record_win(self, hand: Hand) -> None:
        pass

    def record_loss(self, hand: Hand) -> None:
        pass

test_proper = """
    >>> simple = Simple()
"""

from typing import Tuple, Iterator

class LikeAbstract:
    def aMethod(self, arg: int) -> int:
        raise NotImplementedError

# The following will raise a mypy error.
# Chapter_5/ch05_ex1.py:114: error: Signature of "aMethod" incompatible with supertype "LikeAbstract"
class LikeConcrete(LikeAbstract):
    def aMethod(self, arg1: str, arg2: Tuple[int, int]) -> Iterator[Any]:
        pass

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
