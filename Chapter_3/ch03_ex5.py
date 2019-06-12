#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 3. Example 5.
"""

from typing import Iterable, cast, Any, Union, Type, Tuple
import random
from collections import defaultdict
from Chapter_3.ch03_ex1 import card2, Suit, Card2, AceCard2, FaceCard2, NumberCard2
from Chapter_3.ch03_ex3 import Hand, FrozenHand


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


test_float_units = """
    >>> speed = Float_Units(6.8, "knots")
    >>> speed*2
    13.6
    >>> speed.unit
    'knots'
"""

# Option 2...
# A number of casts to work with mypy.
# While this "works" the cast(type, super() doesn't make sense.

from typing import overload, Optional, SupportsFloat, Dict


class Float_Units_Ugly(float):

    unit: str

    def __new__(cls: Type, value: SupportsFloat, unit: str) -> "Float_Units_Ugly":
        # print(f"Float_Units_Ugly {cls}")
        obj = cast("Float_Units_Ugly", cast(type, super()).__new__(cls, float(value)))
        obj.unit = unit
        return obj


test_float_units = """
    >>> speed = Float_Units_Ugly(6.8, "knots")
    >>> speed*2
    13.6
    >>> speed.unit
    'knots'
"""

# Option 3...
# Metaclass to adjust structure.
# Also relevant to the more complex example that follows.


class AddUnitMeta(type):

    def __new__(
        cls: Type, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any], **kwds
    ) -> "Float_Units2":
        namespace["unit"] = None
        result = cast("Float_Units2", super().__new__(cls, name, bases, namespace))
        return result


class Float_Units2(float, metaclass=AddUnitMeta):

    def withUnit(self, unit):
        self.unit = unit
        return self


test_float_units_2 = """
    >>> speed = Float_Units2(6.8).withUnit("knots")
    >>> speed*2
    13.6
    >>> speed.unit
    'knots'
"""

# Metaclass and __new__()
# ===================================

# Example 1. Classes with pre-built loggers.

import logging


class LoggedMeta(type):

    def __new__(
        cls: Type, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]
    ) -> "Logged":
        result = cast("Logged", super().__new__(cls, name, bases, namespace))
        result.logger = logging.getLogger(name)
        return result


class Logged(metaclass=LoggedMeta):
    logger: logging.Logger


class SomeApplicationClass(Logged):

    def __init__(self, v1: int, v2: int) -> None:
        self.logger.info("v1=%r, v2=%r", v1, v2)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v1 * v2
        self.logger.info("product=%r", self.v3)


test_meta = """
    >>> import sys
    >>> logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    >>> sa = SomeApplicationClass(6, 7)
    INFO:SomeApplicationClass:v1=6, v2=7
    INFO:SomeApplicationClass:product=42
    >>> logging.shutdown()
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
