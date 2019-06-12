#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 18. Example 2.
"""

# Command-line parsing
# =======================


# Supply Defaults Via ChainMap built from configuration files and environment variables.


from collections import ChainMap
from typing import Optional, cast, Dict, Any, List, Type
from pathlib import Path
import yaml
import sys
import os
import argparse

from Chapter_18.ch18_ex1 import get_options_1


def nint(x: Optional[str]) -> Optional[int]:
    if x is None:
        return x
    return int(x)


def get_options_2(argv: List[str] = sys.argv[1:]) -> argparse.Namespace:
    """
    Get arguments and options

    :param argv: default sys.argv[1:]
    :return: argparse.Namespace
    """
    # 1. Get files
    config_locations = (
        Path.cwd(),
        Path.home(),
        Path.cwd() / "opt",  # A stand-in for Path("/etc") or Path("/opt")
        Path(__file__) / "config",
        # Other common places...
        # Path("~someapp").expanduser(),
    )

    candidate_paths = (dir / "ch18app.yaml" for dir in config_locations)
    config_paths = (path for path in candidate_paths if path.exists())
    files_values = [yaml.load(str(path)) for path in config_paths]

    # 2. Get potential overrides from the run-time environment
    env_settings = [
        ("samples", nint(os.environ.get("SIM_SAMPLES", None))),
        ("stake", nint(os.environ.get("SIM_STAKE", None))),
        ("rounds", nint(os.environ.get("SIM_ROUNDS", None))),
    ]
    env_values = {k: v for k, v in env_settings if v is not None}

    # 3. Build defaults
    defaults = argparse.Namespace(
        **ChainMap(
            env_values,  # check here first
            *files_values  # All of the files, in order
        )
    )

    # 4. Use the previously-defined argument parser.
    return get_options_1(argv, defaults)


test_env_override = """
    >>> config5a = get_options_2(
    ...        ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"],
    ... )
    >>> config5a
    Namespace(betting_rule='OneThreeTwoSix', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation5.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=100, split_rule='ReSplit', stake=50, verbose=False)

    
    >>> os.environ["SIM_STAKE"] = "100"  # Mock the user's environment
    >>> config5b = get_options_2(
    ...        ["-b", "OneThreeTwoSix", "data/ch18_simulation5.dat"],
    ... )
    >>> config5b
    Namespace(betting_rule='OneThreeTwoSix', dealer_rule='Hit17', decks=6, limit=50, logging_level=20, outputfile='data/ch18_simulation5.dat', payout='(3,2)', player_rule='SomeStrategy', rounds=100, samples=100, split_rule='ReSplit', stake=100, verbose=False)

"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
