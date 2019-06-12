#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 4.
"""

from Chapter_14.simulation_model import *

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union, Dict
import csv
from collections import ChainMap


import io

# JSON or YAML files
# ===================

# JSON using dictionary-of-dictionaries nested structures.
# This is inconvenient to handle multiple configuration files.
import io

json_file = io.StringIO(
    """
{
    "table":{
        "dealer":"Hit17",
        "split":"NoResplitAces",
        "decks":6,
        "limit":50,
        "payout":[3,2]
    },
    "player":{
        "play":"SomeStrategy",
        "betting":"Flat",
        "rounds":100,
        "stake":50
    },
    "simulator":{
        "samples":100,
        "outputfile":"data/ch14_simulation4a.dat"
    }
}
"""
)


def main_nested_dict(config: Dict[str, Any]) -> None:
    dealer_nm = config.get("table", {}).get("dealer", "Hit17")
    dealer_rule = {
        "Hit17": Hit17(),
        "Stand17": Stand17()
    }.get(dealer_nm, Hit17())
    split_nm = config.get("table", {}).get("split", "ReSplit")
    split_rule = {
        "ReSplit": ReSplit(),
        "NoReSplit": NoReSplit(),
        "NoReSplitAces": NoReSplitAces()
    }.get(split_nm, ReSplit())
    decks = config.get("table", {}).get("decks", 6)
    limit = config.get("table", {}).get("limit", 100)
    payout = config.get("table", {}).get("payout", (3, 2))
    table = Table(
        decks=decks, limit=limit, dealer=dealer_rule, split=split_rule, payout=payout
    )

    player_nm = config.get("player", {}).get("play", "SomeStrategy")
    player_rule = {
        "SomeStrategy": SomeStrategy(), "AnotherStrategy": AnotherStrategy()
    }.get(
        player_nm, SomeStrategy()
    )
    bet_nm = config.get("player", {}).get("betting", "Flat")
    betting_rule = {
        "Flat": Flat(), "Martingale": Martingale(), "OneThreeTwoSix": OneThreeTwoSix()
    }.get(
        bet_nm, Flat()
    )
    rounds = config.get("player", {}).get("rounds", 100)
    stake = config.get("player", {}).get("stake", 50)
    player = Player(play=player_rule, betting=betting_rule, max_rounds=rounds, init_stake=stake)

    outputfile = config.get("simulator", {}).get("outputfile", "blackjack.csv")
    samples = config.get("simulator", {}).get("samples", 100)
    simulator = Simulate(table, player, samples)
    with Path(outputfile).open("w", newline="") as results:
        wtr = csv.writer(results)
        for gamestats in simulator:
            wtr.writerow(gamestats)


if __name__ == "__main__":
    import json

    config = json.load(json_file)
    main_nested_dict(config)
    check(Path(config["simulator"]["outputfile"]))

# Flat Version, allows multiple configuration files.
json2_file = io.StringIO(
    """
{
"player.betting": "Flat",
"player.play": "SomeStrategy",
"player.rounds": 100,
"player.stake": 50,
"table.dealer": "Hit17",
"table.decks": 6,
"table.limit": 50,
"table.payout": [3, 2],
"table.split": "NoResplitAces",
"simulator.outputfile": "data/ch14_simulation4b.dat",
"simulator.samples": 100
}
"""
)

json3_file = io.StringIO(
    """
{
"player.betting": "Flat",
"simulator.outputfile": "data/ch14_simulation4b.dat"
}
"""
)

def simulate(table: Table, player: Player, outputpath: Path, samples: int) -> None:
    simulator = Simulate(table, player, samples=samples)
    with outputpath.open("w", newline="") as results:
        wtr = csv.writer(results)
        for gamestats in simulator:
            wtr.writerow(gamestats)

# Using the config to build objects
def main_cm(config: Dict[str, Any]) -> None:
    dealer_nm = config.get("table.dealer", "Hit17")
    dealer_rule = {"Hit17": Hit17(), "Stand17": Stand17()}.get(dealer_nm, Hit17())
    split_nm = config.get("table.split", "ReSplit")
    split_rule = {
        "ReSplit": ReSplit(), "NoReSplit": NoReSplit(), "NoReSplitAces": NoReSplitAces()
    }.get(
        split_nm, ReSplit()
    )
    decks = int(config.get("table.decks", 6))
    limit = int(config.get("table.limit", 100))
    payout = config.get("table.payout", (3, 2))
    table = Table(
        decks=decks, limit=limit, dealer=dealer_rule, split=split_rule, payout=payout
    )

    player_nm = config.get("player.play", "SomeStrategy")
    player_rule = {
        "SomeStrategy": SomeStrategy(), "AnotherStrategy": AnotherStrategy()
    }.get(
        player_nm, SomeStrategy()
    )
    bet_nm = config.get("player.betting", "Flat")
    betting_rule = {
        "Flat": Flat(), "Martingale": Martingale(), "OneThreeTwoSix": OneThreeTwoSix()
    }.get(
        bet_nm, Flat()
    )
    rounds = int(config.get("player.rounds", 100))
    stake = int(config.get("player.stake", 50))
    player = Player(play=player_rule, betting=betting_rule, max_rounds=rounds, init_stake=stake)

    # import yaml
    # print(yaml.dump(vars()))

    outputfile = Path(config.get("simulator.outputfile", "blackjack.csv"))
    samples = int(config.get("simulator.samples", 100))
    simulate(table, player, outputfile, samples)


# Sample Main Script to parse and start the application.
if __name__ == "__main__":
    config_files = json2_file, json3_file,
    config = ChainMap(*[json.load(file) for file in reversed(config_files)])
    print(config)

    main_cm(config)

    check(Path(config.get("simulator.outputfile")))

# YAML
# #######

# Simple YAML
yaml1_file = io.StringIO(
    """
player:
  betting: Flat
  play: SomeStrategy
  rounds: 100
  stake: 50
table:
  dealer: Hit17
  decks: 6
  limit: 50
  payout: [3, 2]
  split: NoResplitAces
simulator: {outputfile: "data/ch14_simulation.dat", samples: 100}
"""
)

import yaml

config = yaml.load(yaml1_file)
if __name__ == "__main__":
    from pprint import pprint

    pprint(config)


yaml1_file = io.StringIO(
    """
# Complete Simulation Settings
table: !!python/object:Chapter_14.simulation_model.Table
  dealer: !!python/object:Chapter_14.simulation_model.Hit17 {}
  decks: 6
  limit: 50
  payout: !!python/tuple [3, 2]
  split: !!python/object:Chapter_14.simulation_model.NoReSplitAces {}
player: !!python/object:Chapter_14.simulation_model.Player
  betting:  !!python/object:Chapter_14.simulation_model.Flat {}
  init_stake: 50
  max_rounds: 100
  play: !!python/object:Chapter_14.simulation_model.SomeStrategy {}
  rounds: 0
  stake: 63.0
samples: 100
outputfile: data/ch14_simulation4c.dat
"""
)

import yaml
if __name__ == "__main__":

    config = yaml.load(yaml1_file)
    print(config)

    simulate(config["table"], config["player"], Path(config["outputfile"]), config["samples"])
    check(Path(config["outputfile"]))



__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
