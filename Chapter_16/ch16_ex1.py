#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 1.
"""

from typing import Type

# Simple Logging
# ==============


class Player:

    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.logger.debug("init bet %r, strategy %r, stake %r", bet, strategy, stake)


# Decorator for Logging
# ========================

# Define a decorator for a class.
# This is confusing to mypy because it's not clear the decorator adds an attribute
# It's not optimal


def logged(cls: Type) -> Type:
    cls.logger = logging.getLogger(cls.__qualname__)
    return cls


import logging
import sys

# Add a level
# ============

logging.addLevelName(15, "VERBOSE")
VERBOSE = 15

# Manual Logging
# ===============

# Mypy is happier. But. We're repeated the class name.
class Player_2:
    logger = logging.getLogger("Player_2")

    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.logger.debug("init bet %s, strategy %s, stake %d", bet, strategy, stake)


# Using a metaclass for consistent logger definition
# ==================================================


class LoggedClassMeta(type):

    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.logger = logging.getLogger(result.__qualname__)
        return result


class LoggedClass(metaclass=LoggedClassMeta):
    logger: logging.Logger


# Sample Class


class Player_3(LoggedClass):

    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.logger.debug("init bet %s, strategy %s, stake %d", bet, strategy, stake)


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    # No configuration -- no output

    logger = logging.getLogger("no_config")
    logger.info("Create Player 2")
    p2 = Player_2("Bet1", "Strategy1", 1)
    logger.info("Create Player 3")
    p3 = Player_3("Bet1", "Strategy1", 1)

    # Configuration changed -- now there's output
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    loggerc = logging.getLogger("config")
    loggerc.info("Create Player")
    pc = Player("Bet", "Strategy", 10)
    loggerc.info("Create Player 2")
    pc2 = Player_2("Bet2", "Strategy2", 2)
    loggerc.info("Create Player 3")
    pc3 = Player_3("Bet3", "Strategy3", 3)

    logging.shutdown()
