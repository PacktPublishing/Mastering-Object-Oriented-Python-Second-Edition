#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 2.
"""

from typing import Type
import logging
import sys


# Multiple Loggers
# ===========================


# This is confusing to mypy because it's not clear the decorator adds attributes.

def log_to(*names: str):
    if len(names) == 0:
        names = ('logger',)

    def concrete_log_to(cls: Type) -> Type:
        for log_name in names:
            setattr(cls, log_name, logging.getLogger(
                f"{log_name}.{cls.__qualname__}"))
        return cls

    return concrete_log_to

# Sample Class

# Chapter_16/ch16_ex2.py:41: error: "Player" has no attribute "audit"
# Chapter_16/ch16_ex2.py:42: error: "Player" has no attribute "verbose"

@log_to("audit", "verbose")
class Player:
    def __init__(self, bet: str, strategy: str, stake: int) -> None:
        self.audit.info(f"Initial {stake:d}")
        self.verbose.info(f"Init bet={bet:s} strategy={strategy:s} stake={stake:d}")

# Chapter_16/ch16_ex2.py:50: error: "Table" has no attribute "security"

@log_to("security")
class Table:
    def add_player(self, player: Player) -> None:
        self.security.info(f"Adding {player}")

# Demo Output

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, style="{")

print("Create Player 2")
p3 = Player("Bet3", "Strategy3", 3)
t = Table()
t.add_player(p3)

logging.shutdown()



__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
