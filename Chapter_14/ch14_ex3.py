#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 3.
"""

from Chapter_14.simulation_model import *
from pprint import pprint

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union, Dict
import typing
import csv
from types import SimpleNamespace

def simulate(table: Table, player: Player, outputpath: Path, samples: int) -> None:
    simulator = Simulate(table, player, samples=samples)
    with outputpath.open("w", newline="") as results:
        wtr = csv.writer(results)
        for gamestats in simulator:
            wtr.writerow(gamestats)

# Exec Import
# ################

import io

py_file = io.StringIO(
"""
# SomeStrategy setup

# Table
dealer_rule = Hit17()
split_rule = NoReSplitAces()
table = Table(decks=6, limit=50, dealer=dealer_rule,
        split=split_rule, payout=(3,2))

# Player
player_rule = SomeStrategy()
betting_rule = Flat()
player = Player(play=player_rule, betting=betting_rule,
        max_rounds=100, init_stake=50)

# Simulation
outputfile = Path.cwd()/"data"/"ch14_simulation3a.dat"
samples = 100
"""
)

if __name__ == "__main__":
    code = compile(py_file.read(), "stringio", "exec")
    assignments: Dict[str, Any] = dict()
    exec(code, globals(), assignments)
    config = SimpleNamespace(**assignments)

    print("Exec Import...")
    pprint(assignments)
    print("Table...")
    print(config.table)

    simulate(config.table, config.player, config.outputfile, config.samples)
    check(config.outputfile)

# ChainMap and Import
# =====================

# Essential Example
from collections import ChainMap

config_name = "config.py"
config_locations = (
    Path.cwd(),
    Path.home(),
    Path("/etc/thisapp"),
    # Optionally Path("~thisapp").expanduser(), when an app has a "home" directory
    Path(__file__),
)

candidates = (dir / config_name for dir in config_locations)
config_paths = (path for path in candidates if path.exists())
cm_config_1: typing.ChainMap[str, Any] = ChainMap()
for path in config_paths:
    config_layer_1: Dict[str, Any] = {}
    source_code = path.read_text()
    exec(source_code, globals(), config_layer_1)
    cm_config_1.maps.append(config_layer_1)

# Demo with Mock files
import io

py_text = """
# Default casino rules
# Table
dealer_rule = Hit17()
split_rule = NoReSplitAces()
table = Table(decks=6, limit=50, dealer=dealer_rule,
        split=split_rule, payout=(3,2))

# Player
player_rule = SomeStrategy()
betting_rule = Flat()
player = Player(play=player_rule, betting=betting_rule,
        max_rounds=100, init_stake=50)

# Simulation
outputfile = Path.cwd()/"data"/"ch14_simulation3b.dat"
samples = 100
"""

py2_text = """
# Override values
# Player
player_rule = AnotherStrategy()
betting_rule = Martingale()
player = Player(play=player_rule, betting=betting_rule,
        max_rounds=100, init_stake=50)

# Simulation
outputfile = Path.cwd()/"data"/"ch14_simulation3b.dat"
"""

test_cm_config = """
>>> default_file = io.StringIO(py_text)
>>> override_file = io.StringIO(py2_text)
>>> cm_config: typing.ChainMap[str, Any] = ChainMap()
>>> for path in override_file, default_file:
...     config_layer: Dict[str, Any] = {}
...     source_code = path.read()
...     exec(source_code, globals(), config_layer)
...     cm_config.maps.append(config_layer)
>>> cm_config['player_rule']  # doctest: +ELLIPSIS
AnotherStrategy()
>>> cm_config['betting_rule']  # doctest: +ELLIPSIS
Martingale()
>>> cm_config['betting_rule'] = "final override"
>>> pprint(cm_config)  # doctest: +ELLIPSIS
ChainMap({'betting_rule': 'final override'},
         {'betting_rule': Martingale(),
          'outputfile': PosixPath('.../data/ch14_simulation3b.dat'),
          'player': Player(play=AnotherStrategy(), betting=Martingale(), max_rounds=100, init_stake=50, rounds=100, stake=50),
          'player_rule': AnotherStrategy()},
         {'betting_rule': Flat(),
          'dealer_rule': Hit17(),
          'outputfile': PosixPath('.../data/ch14_simulation3b.dat'),
          'player': Player(play=SomeStrategy(), betting=Flat(), max_rounds=100, init_stake=50, rounds=100, stake=50),
          'player_rule': SomeStrategy(),
          'samples': 100,
          'split_rule': NoReSplitAces(),
          'table': Table(decks=6, limit=50, dealer=Hit17(), split=NoReSplitAces(), payout=(3, 2))})
"""

if __name__ == "__main__":
    default_file = io.StringIO(py_text)
    override_file = io.StringIO(py2_text)
    cm_config: typing.ChainMap[str, Any] = ChainMap()
    for config_file in override_file, default_file:
        config_layer: Dict[str, Any] = {}
        source_code = config_file.read()
        exec(source_code, globals(), config_layer)
        cm_config.maps.append(config_layer)

    print()
    print("ChainMap")
    pprint(cm_config)


class AttrChainMap(ChainMap):

    def __getattr__(self, name: str) -> Any:
        if name == "maps":
            return self.__dict__["maps"]
        return super().get(name, None)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "maps":
            self.__dict__["maps"] = value
            return
        self[name] = value

test_acm_config = """
>>> default_file = io.StringIO(py_text)
>>> override_file = io.StringIO(py2_text)
>>> acm_config = AttrChainMap()
>>> for path in override_file, default_file:
...     config_layer: Dict[str, Any] = {}
...     source_code = path.read()
...     exec(source_code, globals(), config_layer)
...     acm_config.maps.append(config_layer)
>>> acm_config['player_rule']  # doctest: +ELLIPSIS
AnotherStrategy()
>>> acm_config.player_rule  # doctest: +ELLIPSIS
AnotherStrategy()
>>> acm_config.betting_rule  # doctest: +ELLIPSIS
Martingale()
"""

if __name__ == "__main__":

    default_file = io.StringIO(py_text)
    override_file = io.StringIO(py2_text)
    config_acm = AttrChainMap()
    for file in override_file, default_file:
        config_layer = {}
        config_source = file.read()
        exec(config_source, globals(), config_layer)
        config_acm.maps.append(config_layer)

    print()
    print("AttrChainMap")
    pprint(config_acm)
    print(config_acm.table)
    print(config_acm["table"])

    simulate(config_acm.table, config_acm.player, config_acm.outputfile, config_acm.samples)
    check(config_acm.outputfile)

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
