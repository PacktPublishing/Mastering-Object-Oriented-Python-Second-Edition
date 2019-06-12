#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 18. Example 1.
"""

import os

# Command-line parsing
# =======================

import argparse
import sys
import logging
from typing import List, Optional

__version__ = "2e"


def get_options_1(
    argv: List[str] = sys.argv[1:], defaults: Optional[argparse.Namespace] = None
) -> argparse.Namespace:
    """
    Parse command-line arguments and options

    :param argv: Command line, default ``sys.argv[1:]``
    :param defaults: an ``argparse.Namespace`` with defaults
    :return: argparse.Namespace with parameters
    """
    # Step 1: Parser.

    parser = argparse.ArgumentParser(
        prog="ch18_ex1.py",
        description="Simulate Blackjack",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Step 2: Arguments.

    # Simple on-off options

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument(
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        dest="logging_level",
    )

    # Options with values

    parser.add_argument(
        "--dealerhit",
        action="store",
        default="Hit17",
        choices=["Hit17", "Stand17"],
        dest="dealer_rule",
    )
    parser.add_argument(
        "--resplit",
        action="store",
        default="ReSplit",
        choices=["ReSplit", "NoReSplit", "NoReSplitAces"],
        dest="split_rule",
    )

    parser.add_argument(
        "--decks", action="store", default=6, type=int, help="Decks to deal"
    )
    parser.add_argument("--limit", action="store", default=50, type=int)
    parser.add_argument("--payout", action="store", default="(3,2)")

    parser.add_argument(
        "-p",
        "--playerstrategy",
        action="store",
        default="SomeStrategy",
        choices=["SomeStrategy", "AnotherStrategy"],
        dest="player_rule",
    )
    parser.add_argument(
        "-b",
        "--bet",
        action="store",
        default="Flat",
        choices=["Flat", "Martingale", "OneThreeTwoSix"],
        dest="betting_rule",
    )
    parser.add_argument("-r", "--rounds", action="store", default=100, type=int)
    parser.add_argument("-s", "--stake", action="store", default=50, type=int)

    parser.add_argument(
        "--samples",
        action="store",
        default=int(os.environ.get("SIM_SAMPLES", 100)),
        type=int,
        help="Samples to generate",
    )

    # Arguments

    parser.add_argument("outputfile", action="store", metavar="output")  # required

    # Version and help

    parser.add_argument("-V", "--version", action="version", version=__version__)
    parser.add_argument("-?", "--help", action="help")

    # Step 3: Parse

    return parser.parse_args(argv, namespace=defaults)


# Examples

test_parsing_1 = """
    >>> config1 = get_options_1(
    ...     ["data/ch18_simulation1.dat"]
    ... )
    >>> config1
    Namespace(betting_rule='Flat', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation1.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=100, split_rule='ReSplit', stake=50, verbose=False)
    
    >>> config2 = get_options_1(
    ...     ["-v", "--samples", "2", "data/ch18_simulation2.dat"]
    ... )
    >>> config2
    Namespace(betting_rule='Flat', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation2.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=2, split_rule='ReSplit', stake=50, verbose=True)
    
    >>> config3 = get_options_1(
    ...     ["-b", "Martingale", "--samples", "3", "data/ch18_simulation3.dat"]
    ... )
    >>> config3
    Namespace(betting_rule='Martingale', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation3.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=3, split_rule='ReSplit', stake=50, verbose=False)
    
    >>> import shlex
    >>> config4 = get_options_1(
    ...     shlex.split("-b Martingale --samples 3 data/ch18_simulation3.dat")
    ... )
    >>> config4
    Namespace(betting_rule='Martingale', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation3.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=3, split_rule='ReSplit', stake=50, verbose=False)
"""

import pytest


def test_get_config_1(capsys):

    with pytest.raises(SystemExit) as exception:
        get_options_1(
            ["-b", "Doesn't Work", "--samples", "x", "data/ch18_simulation3.dat"]
        )

    assert exception.value.args == (2,)
    out, err = capsys.readouterr()
    expected_err = """\
usage: ch18_ex1.py [-v] [--debug] [--dealerhit {Hit17,Stand17}]
                   [--resplit {ReSplit,NoReSplit,NoReSplitAces}]
                   [--decks DECKS] [--limit LIMIT] [--payout PAYOUT]
                   [-p {SomeStrategy,AnotherStrategy}]
                   [-b {Flat,Martingale,OneThreeTwoSix}] [-r ROUNDS]
                   [-s STAKE] [--samples SAMPLES] [-V] [-?]
                   output
ch18_ex1.py: error: argument -b/--bet: invalid choice: "Doesn't Work" (choose from 'Flat', 'Martingale', 'OneThreeTwoSix')
"""
    assert expected_err == err


# Supplying Defaults
# =====================

# Simple

config4 = argparse.Namespace()
config4.dealer_rule = "Hit17"
config4.split_rule = "NoReSplitAces"
config4.limit = 50
config4.decks = 6
config4.payout = "(3,2)"
config4.player_rule = "SomeStrategy"
config4.betting_rule = "Flat"
config4.rounds = 100
config4.stake = 50
config4.outputfile = "data/ch18_simulation4.dat"
config4.samples = int(os.environ.get("SIM_SAMPLES", 200))

test_parsing_2 = """
    >>> config5 = get_options_1(
    ...    ["-b", "OneThreeTwoSix", "data/ch18_simulation4.dat"], defaults=config4
    ... )
    >>> config5
    Namespace(betting_rule='OneThreeTwoSix', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation4.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=200, split_rule='NoReSplitAces', stake=50, verbose=False)
"""

# Path manipulations
# ===================

from pathlib import Path

test_path_examples = """
    >>> p = Path.cwd() / "data" / "simulation.csv"
    >>> p.name
    'simulation.csv'
    >>> p.suffix
    '.csv'
    >>> p.exists()
    False
"""

test_path_example2 = """
    >>> source_path = Path("data")/"ch14_simulation.dat"
    >>> with source_path.open() as source_file:
    ...     count = 0
    ...     for line in source_file:
    ...         if len(line) > 0:
    ...              count += 1
    >>> count
    100
"""

test_path_example3 = """
    >>> if (Path("data")/"ch18_directory").exists():
    ...     (Path("data")/"ch18_directory").rmdir()
    
    >>> target = Path("data")/"ch18_directory"
    >>> target.mkdir(exist_ok=True, parents=True)
    >>> (Path("data")/"ch18_directory").exists()
    True
    
    >>> import datetime
    >>> today = datetime.datetime.today()
    >>> today = datetime.datetime(2019, 3, 18)
    >>> target = Path("data")/today.strftime("%Y%m%d")
    >>> target.mkdir(exist_ok=True, parents=True)
    >>> target.exists()
    True
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    import pytest

    pytest.main(["Chapter_18/ch18_ex1.py"])

    get_options_1(['--help'])
