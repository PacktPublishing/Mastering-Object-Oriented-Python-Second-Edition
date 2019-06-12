#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 1.
"""

from Chapter_14.simulation_model import *

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union
import csv


def simulate_blackjack() -> None:
    dealer_rule = Hit17()
    split_rule = NoReSplitAces()
    table = Table(
        decks=6, limit=50, dealer=dealer_rule,
        split=split_rule, payout=(3, 2)
    )
    player_rule = SomeStrategy()
    betting_rule = Flat()
    player = Player(
        play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50
    )

    simulator = Simulate(
        table, player, samples=100
    )
    result_path = Path.cwd() / "data" / "ch14_simulation.dat"
    with result_path.open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(simulator)


if __name__ == "__main__":
    simulate_blackjack()
    check(Path.cwd() / "data" / "ch14_simulation.dat")

# Locations
# ============

# Tyical list of locations for config

def location_list(config_name: str = "someapp.config") -> List[Path]:
    config_locations = (
        Path(__file__),
        # Path("~someapp").expanduser(), if a special username
        Path("/opt") / "someapp",
        Path("/etc") / "someapp",
        Path.home(),
        Path.cwd(),
    )
    candidates = (dir / config_name for dir in config_locations)
    config_paths = [path for path in candidates if path.exists()]
    return config_paths

test_location_list = """
>>> import os
>>> previous = os.getcwd()
>>> os.chdir("Chapter_14")
>>> location_list()  # doctest: +ELLIPSIS
[PosixPath('.../Chapter_14/someapp.config')]
>>> os.chdir(previous)
"""

# INI files
# =========

# Sample INI files
import io

ini_file = io.StringIO(
    """
; Default casino rules
[table]
    dealer= Hit17
    split= NoResplitAces
    decks= 6
    limit= 50
    payout= (3,2)

; Player with SomeStrategy
[player]
    play= SomeStrategy
    betting= Flat
    max_rounds= 100
    init_stake= 50

[simulator]
    samples= 100
    outputfile= data/ch14_simulation1.dat
"""
)

ini2_file = io.StringIO(
    """
; Need to compare with OtherStrategy
[player]
    play= OtherStrategy
    betting= Flat
    max_rounds= 100
    init_stake= 50

[simulator]
    samples= 100
    outputfile= data/ch14_simulation1a.dat
"""
)

import configparser

# Using the config to build objects
def main_ini(config: configparser.ConfigParser) -> None:
    dealer_nm = config.get("table", "dealer", fallback="Hit17")
    dealer_rule = {
        "Hit17": Hit17(),
        "Stand17": Stand17(),
    }.get(dealer_nm, Hit17())
    split_nm = config.get("table", "split", fallback="ReSplit")
    split_rule = {
        "ReSplit": ReSplit(),
        "NoReSplit": NoReSplit(),
        "NoReSplitAces": NoReSplitAces(),
    }.get(split_nm, ReSplit())
    decks = config.getint("table", "decks", fallback=6)
    limit = config.getint("table", "limit", fallback=100)
    payout = eval(
        config.get("table", "payout", fallback="(3,2)")
    )
    table = Table(
        decks=decks, limit=limit, dealer=dealer_rule,
        split=split_rule, payout=payout
    )

    player_nm = config.get(
        "player", "play", fallback="SomeStrategy")
    player_rule = {
        "SomeStrategy": SomeStrategy(),
        "AnotherStrategy": AnotherStrategy()
    }.get(player_nm, SomeStrategy())
    bet_nm = config.get("player", "betting", fallback="Flat")
    betting_rule = {
        "Flat": Flat(),
        "Martingale": Martingale(),
        "OneThreeTwoSix": OneThreeTwoSix()
    }.get(bet_nm, Flat())
    max_rounds = config.getint("player", "max_rounds", fallback=100)
    init_stake = config.getint("player", "init_stake", fallback=50)
    player = Player(
        play=player_rule, betting=betting_rule,
        max_rounds=max_rounds, init_stake=init_stake
    )

    outputfile = config.get(
        "simulator", "outputfile", fallback="blackjack.csv")
    samples = config.getint("simulator", "samples", fallback=100)
    simulator = Simulate(table, player, samples=samples)
    with Path(outputfile).open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(simulator)


# Sample Main Script to parse and start the application.
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read_file(ini_file)
    config.read_file(ini2_file)

    # Could use config.read_string(text), also
    # When there are multiple candidate locations, config.read(location_list("blackjack.ini"))

    for name, section in config.items():
        print(name)
        for p in config.items(name):
            print(" ", p)

    main_ini(config)
    check(Path(config.get("simulator", "outputfile")))

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
