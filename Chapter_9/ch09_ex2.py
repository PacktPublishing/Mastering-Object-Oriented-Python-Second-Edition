#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 9. Example 2.
"""
from typing import Any, Type

# Class Decorator 2 -- Logger
# ==============================

import logging
import sys

# Wordy - but visible to mypy
class UglyClass1:

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


# Non-DRY -- class name is repeated
class UglyClass2:
    logger = logging.getLogger("UglyClass2")

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


# Less Ugly, more DRY
# However... mypy can't see this attribute -- not a solution
# Chapter_9/ch09_ex2.py:54: error: "SomeClass" has no attribute "logger"
# Chapter_9/ch09_ex2.py:57: error: "SomeClass" has no attribute "logger"
def logged(class_: Type) -> Type:
    class_.logger = logging.getLogger(class_.__qualname__)
    return class_


@logged
class SomeClass:

    def __init__(self) -> None:
        self.logger.info("New thing")  # mypy error

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)  # mypy error
        return 42


# More DRY. And visible to mypy.
class LoggedInstance:
    logger: logging.Logger

    def __new__(cls):
        instance = super().__new__(cls)
        instance.logger = logging.getLogger(cls.__qualname__)
        return instance


class SomeClass2(LoggedInstance):

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


# And a class-level logger, just to be complete.


class LoggedClassMeta(type):

    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.logger = logging.getLogger(result.__qualname__)
        return result


class LoggedClass(metaclass=LoggedClassMeta):
    logger: logging.Logger
    pass


class SomeClass3(LoggedClass):

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


class LoggedWithHook:
    def __init_subclass__(cls, name=None):
        cls.logger = logging.getLogger(name or cls.__qualname__)


class SomeClass4(LoggedWithHook):

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42

class SomeClass4s(LoggedWithHook, name='special'):

    def __init__(self) -> None:
        self.logger.info("New thing")

    def method(self, *args: Any) -> int:
        self.logger.info("method %r", args)
        return 42


test_logged_class = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    >>> uc1 = UglyClass1()
    >>> uc1.method(355 / 113)
    42
    >>> uc2 = UglyClass2()
    >>> uc2.method(355 / 113)
    42
    >>> sc = SomeClass()
    >>> sc.method(355 / 113)
    42
    >>> sc2 = SomeClass2()
    >>> sc2.method(355 / 113)
    42
    >>> sc3 = SomeClass3()
    >>> sc3.method(355 / 113)
    42
    >>> sc4 = SomeClass4()
    >>> sc4.method(365 / 113)
    42
    >>> sc4s = SomeClass4s()
    >>> sc4s.method(365 / 113)
    42
    >>> logging.shutdown()
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
