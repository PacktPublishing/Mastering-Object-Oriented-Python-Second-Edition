#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 5.
"""
from typing import Type, Dict
import logging
import logging.config
import yaml

# A context manager can be used, also.
# Note that there are profound limitations when using dictConfig.
# Any loggers created prior to running dictConfig wind up disconnected.
# Be sure to include ``disable_existing_loggers: False`` in the dictionary.


# Debugging
# ==================

# New Config

config5 = """
version: 1
disable_existing_loggers: False
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stderr
    formatter: basic
  audit_file:
    class: logging.FileHandler
    filename: data/ch16_audit.log
    encoding: utf-8
    formatter: detailed
formatters:
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
  detailed:
    style: "{"
    format: "{levelname:s}:{name:s}:{asctime:s}:{message:s}"
    datefmt: "%Y-%m-%d %H:%M:%S"
loggers:
  audit:
    handlers: [console,audit_file]
    level: INFO
    propagate: False
root:
  handlers: [console]
  level: INFO
disable_existing_loggers: False
"""


# Some classes
from Chapter_16.ch16_ex1 import LoggedClass


class BettingStrategy(LoggedClass):

    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class OneThreeTwoSix(BettingStrategy):

    def __init__(self) -> None:
        self.wins = 0

    def _state(self) -> Dict[str, int]:
        return dict(wins=self.wins)

    def bet(self) -> int:
        bet = {0: 1, 1: 3, 2: 2, 3: 6}[self.wins % 4]
        self.logger.debug(f"Bet {self._state()}; based on {bet}")
        return bet

    def record_win(self) -> None:
        self.wins += 1
        self.logger.debug(f"Win: {self._state()}")

    def record_loss(self) -> None:
        self.wins = 0
        self.logger.debug(f"Loss: {self._state()}")


# A Decorator -- This confuses mypy


def audited(cls: Type) -> Type:
    cls.logger = logging.getLogger(cls.__qualname__)
    cls.audit = logging.getLogger(f"audit.{cls.__qualname__}")
    return cls


# A metaclass -- Much easier on mypy
# Extending the basic logged class meta to add yet more features

from Chapter_16.ch16_ex1 import LoggedClassMeta

class AuditedClassMeta(LoggedClassMeta):

    def __new__(cls, name, bases, namespace, **kwds):
        result = LoggedClassMeta.__new__(cls, name, bases, dict(namespace))
        for item, type_ref in result.__annotations__.items():
            if issubclass(type_ref, logging.Logger):
                prefix = "" if item == "logger" else f"{item}."
                logger = logging.getLogger(f"{prefix}{result.__qualname__}")
                setattr(result, item, logger)
        return result


class AuditedClass(LoggedClass, metaclass=AuditedClassMeta):
    audit: logging.Logger
    pass


class Table(AuditedClass):

    def bet(self, bet: str, amount: int) -> None:
        self.logger.info("Betting %d on %s", amount, bet)
        self.audit.info("Bet:%r, Amount:%r", bet, amount)


# A Main Program demo

import atexit

logging.config.dictConfig(yaml.load(config5))
atexit.register(logging.shutdown)
log = logging.getLogger("main")
log.info("Starting")
strategy = OneThreeTwoSix()
application = Table()
application.bet("Black", strategy.bet())
strategy.record_win()
application.bet("Black", strategy.bet())
strategy.record_win()
application.bet("Black", strategy.bet())
strategy.record_loss()
application.bet("Black", strategy.bet())
log.info("Finish")
logging.shutdown()


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
