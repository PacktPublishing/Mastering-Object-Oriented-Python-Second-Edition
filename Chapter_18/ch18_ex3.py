#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 18. Example 3.
"""

# Preliminary Definitions
# ========================

# Import the simulation model we've been using.
# Plus a handy validation function that assures the output is sensible.
# And logging, since we'll use it for some examples.

from Chapter_14.simulation_model import *

import logging
from pprint import pprint
from pathlib import Path
import os


# Top-level Function
# ===================

# Here's the main feature of a program as a top-level function.


import ast
import csv
import argparse


def simulate_blackjack(config: argparse.Namespace) -> None:
    dealer_classes = {"Hit17": Hit17, "Stand17": Stand17}
    dealer_rule = dealer_classes[config.dealer_rule]()
    split_classes = {
        "ReSplit": ReSplit, "NoReSplit": NoReSplit, "NoReSplitAces": NoReSplitAces
    }
    split_rule = split_classes[config.split_rule]()
    try:
        payout = ast.literal_eval(config.payout)
        assert len(payout) == 2
    except Exception as ex:
        raise ValueError(f"Invalid payout {config.payout}") from ex
    table = Table(
        decks=config.decks,
        limit=config.limit,
        dealer=dealer_rule,
        split=split_rule,
        payout=payout,
    )
    player_classes = {"SomeStrategy": SomeStrategy, "AnotherStrategy": AnotherStrategy}
    player_rule = player_classes[config.player_rule]()
    betting_classes = {
        "Flat": Flat, "Martingale": Martingale, "OneThreeTwoSix": OneThreeTwoSix
    }
    betting_rule = betting_classes[config.betting_rule]()
    player = Player(
        play=player_rule,
        betting=betting_rule,
        max_rounds=config.rounds,
        init_stake=config.stake,
    )
    simulate = Simulate(table, player, config.samples)
    with Path(config.outputfile).open("w", newline="") as target:
        wtr = csv.writer(target)
        wtr.writerows(simulate)


# Using the top-level function

from Chapter_18.ch18_ex2 import get_options_2

if __name__ == "__main__":
    arguments = ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"]
    config_1 = get_options_2(arguments)
    simulate_blackjack(config_1)
    check(Path.cwd() / "data" / "ch18_simulation5.dat")


# Here's how we can build the configuration as a context manager.
# It's consistent with using a context manager for logging setup.

from typing import List


class Build_Config:

    def __init__(self, argv: List[str]) -> None:
        self.options = get_options_2(argv)

    def __enter__(self) -> argparse.Namespace:
        return self.options

    def __exit__(self, *exc) -> None:
        return


# Using the top-level function with a context manager that collects
# the configuration.

if __name__ == "__main__":
    arguments = ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"]
    with Build_Config(arguments) as config_2:
        simulate_blackjack(config_2)
        check(Path.cwd() / "data" / "ch18_simulation5.dat")

# Logging and config as context
# ===============================


import logging.config
import sys

# Here's logging setup as a context manager.


class Setup_Logging:

    def __init__(self, stream=sys.stderr, disable_existing_loggers=False) -> None:
        """
        Preserves existing loggers.
        """
        self.config = dict(
            version=1,
            handlers={
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": stream,
                    "formatter": "basic",
                }
            },
            formatters={
                "basic": {"format": "{name} ({levelname}) {message}", "style": "{"}
            },
            root={"handlers": ["console"], "level": logging.INFO},
            disable_existing_loggers=disable_existing_loggers,
        )

    def __enter__(self) -> "Setup_Logging":
        logging.config.dictConfig(self.config)
        return self

    def __exit__(self, *exc) -> None:
        logging.shutdown()
        return


# The downside of using a dictConfig as a context manager is that
# logging objects created before logging is configured don't connect.
# properly to the root logger with usable handlers.


class ClassLogger:
    log = logging.getLogger("ClassLogger")

    def work(self) -> None:
        self.log.info("Some Info")
        self.log.warning("A Warning")


class InstanceLogger:

    def __init__(self, name: str) -> None:
        self.log = logging.getLogger(f"InstanceLogger.{name}")

    def work(self) -> None:
        self.log.info("Some Info")
        self.log.warning("A Warning")


# Here's a main function that uses two nested contexts.

test_nested_contexts_1 = """
    Loggers created outside the context
    *will* be ignored because disable_existing_loggers is True.
    This includes loggers in class definitions.
    
    >>> il_early = InstanceLogger("ignored")
    >>> with Setup_Logging(disable_existing_loggers=True, stream=sys.stdout):
    ...     cl = ClassLogger()
    ...     il = InstanceLogger("good")
    ...     cl.work()
    ...     il.work()
    ...     il_early.work()
    InstanceLogger.good (INFO) Some Info
    InstanceLogger.good (WARNING) A Warning
"""

test_nested_contexts_2 = """
    All loggers *will* be used because disable_existing_loggers is False
    
    >>> il_early = InstanceLogger("retained")
    >>> with Setup_Logging(disable_existing_loggers=False, stream=sys.stdout):
    ...     cl = ClassLogger()
    ...     il = InstanceLogger("good")
    ...     cl.work()
    ...     il.work()
    ...     il_early.work()
    ClassLogger (INFO) Some Info
    ClassLogger (WARNING) A Warning
    InstanceLogger.good (INFO) Some Info
    InstanceLogger.good (WARNING) A Warning
    InstanceLogger.retained (INFO) Some Info
    InstanceLogger.retained (WARNING) A Warning
"""


# PITL via Function Composition
# =======================================

# Example of adding features through more
# top-level functions.


def simulate_blackjack_betting(config: argparse.Namespace) -> None:
    for bet_class in "Flat", "Martingale", "OneThreeTwoSix":
        config.betting_rule = bet_class
        config.outputfile = Path("data")/f"ch18_simulation6_{bet_class}.dat"
        simulate_blackjack(config)


# This works reasonably well. We can do a bit more with object
# composition.

# Top script

if __name__ == "__main__":
    arguments = ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"]
    with Setup_Logging():
        with Build_Config(arguments) as config_3:
            simulate_blackjack_betting(config_3)
    check(Path.cwd() / "data" / "ch18_simulation6_Flat.dat")
    check(Path.cwd() / "data" / "ch18_simulation6_Martingale.dat")
    check(Path.cwd() / "data" / "ch18_simulation6_OneThreeTwoSix.dat")

# PITL via Object Composition
# =======================================

# Proper **Command** design pattern

from typing import Dict, Any, Type


class Command:
    """
    Typical use

    >>> c = Command()
    >>> c.configure(argparse.Namespace(item="value"))
    >>> c.run()
    """

    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}

    def configure(self, namespace: argparse.Namespace) -> None:
        self.config.update(vars(namespace))

    def run(self) -> None:
        """Overridden by a subclass"""
        pass


class Simulate_Command(Command):
    dealer_rule_map = {"Hit17": Hit17, "Stand17": Stand17}
    split_rule_map = {
        "ReSplit": ReSplit, "NoReSplit": NoReSplit, "NoReSplitAces": NoReSplitAces
    }
    player_rule_map = {"SomeStrategy": SomeStrategy, "AnotherStrategy": AnotherStrategy}
    betting_rule_map = {
        "Flat": Flat, "Martingale": Martingale, "OneThreeTwoSix": OneThreeTwoSix
    }

    def run(self) -> None:
        dealer_rule = self.dealer_rule_map[self.config["dealer_rule"]]()
        split_rule = self.split_rule_map[self.config["split_rule"]]()
        payout: Tuple[int, int]
        try:
            payout = ast.literal_eval(self.config["payout"])
            assert len(payout) == 2
        except Exception as e:
            raise Exception(f"Invalid payout {self.config['payout']!r}") from e
        table = Table(
            decks=self.config["decks"],
            limit=self.config["limit"],
            dealer=dealer_rule,
            split=split_rule,
            payout=payout,
        )
        player_rule = self.player_rule_map[self.config["player_rule"]]()
        betting_rule = self.betting_rule_map[self.config["betting_rule"]]()
        player = Player(
            play=player_rule,
            betting=betting_rule,
            max_rounds=self.config["rounds"],
            init_stake=self.config["stake"],
        )
        simulate = Simulate(table, player, self.config["samples"])
        with Path(self.config["outputfile"]).open("w", newline="") as target:
            wtr = csv.writer(target)
            wtr.writerows(simulate)


if __name__ == "__main__":
    arguments = ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"]
    with Setup_Logging():
        with Build_Config(arguments) as config_4:
            main = Simulate_Command()
            main.configure(config_4)
            main.run()


# Composition


class Analyze_Command(Command):

    def run(self) -> None:
        with Path(self.config["outputfile"]).open() as target:
            rdr = csv.reader(target)
            outcomes = (float(row[10]) for row in rdr)
            first = next(outcomes)
            sum_0, sum_1 = 1, first
            value_min = value_max = first
            for value in outcomes:
                sum_0 += 1  # value**0
                sum_1 += value  # value**1
                value_min = min(value_min, value)
                value_max = max(value_max, value)
            mean = sum_1 / sum_0
            print(
                f"{self.config['outputfile']}\n"
                f"Mean = {mean:.1f}\n"
                f"House Edge = {1 - mean / 50:.1%}\n"
                f"Range = {value_min:.1f} {value_max:.1f}"
            )


class Command_Sequence(Command):
    """
    Subclass provides a sequence of classes. These will be expanded into instance and configured.
    """
    steps: List[Type[Command]] = []

    def __init__(self) -> None:
        self._sequence = [class_() for class_ in self.steps]

    def configure(self, config: argparse.Namespace) -> None:
        for step in self._sequence:
            step.configure(config)

    def run(self) -> None:
        for step in self._sequence:
            step.run()


class Simulate_and_Analyze(Command_Sequence):
    steps = [Simulate_Command, Analyze_Command]


if __name__ == "__main__":
    with Build_Config(arguments) as config_5:
        both = Simulate_and_Analyze()
        both.configure(config_5)
        both.run()
    check(Path.cwd() / "data" / "ch18_simulation6_Flat.dat")
    check(Path.cwd() / "data" / "ch18_simulation6_Martingale.dat")
    check(Path.cwd() / "data" / "ch18_simulation6_OneThreeTwoSix.dat")


# Wrapping another class in a For-All loop.


class ForAllBets_Simulate(Command):

    def run(self) -> None:
        for bet_class in "Flat", "Martingale", "OneThreeTwoSix":
            self.config["betting_rule"] = bet_class
            self.config["outputfile"] = Path("data")/f"ch18_simulation7_{bet_class}.dat"
            sim = Simulate_Command()
            # sim.config = self.config  # Push the configuration directly.
            sim.configure(argparse.Namespace(**self.config))
            sim.run()


if __name__ == "__main__":
    with Build_Config(arguments) as config_6:
        msc = ForAllBets_Simulate()
        msc.configure(config_6)
        msc.run()
    check(Path.cwd() / "data" / "ch18_simulation7_Flat.dat")
    check(Path.cwd() / "data" / "ch18_simulation7_Martingale.dat")
    check(Path.cwd() / "data" / "ch18_simulation7_OneThreeTwoSix.dat")


# Overall doctest

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
