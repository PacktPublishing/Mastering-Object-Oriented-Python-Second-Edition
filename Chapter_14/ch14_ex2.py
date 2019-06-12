#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 2.
"""

from Chapter_14.simulation_model import *

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union, Type
import csv
from dataclasses import dataclass
from types import SimpleNamespace

# PY files
# ========

# Top-level -- v1
# ################


def simulate(table: Table, player: Player, outputpath: Path, samples: int) -> None:
    simulator = Simulate(table, player, samples=samples)
    with outputpath.open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(simulator)


# Configuration in the main script
#
# ``from simulator import *``
#
def simulate_SomeStrategy_Flat() -> None:
    dealer_rule = Hit17()
    split_rule = NoReSplitAces()
    table = Table(
        decks=6, limit=50, dealer=dealer_rule, split=split_rule, payout=(3, 2)
    )
    player_rule = SomeStrategy()
    betting_rule = Flat()
    player = Player(
        play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50
    )
    simulate(table, player, Path.cwd() / "data" / "ch14_simulation2a.dat", 100)


if __name__ == "__main__":
    simulate_SomeStrategy_Flat()
    check(Path.cwd() / "data" / "ch14_simulation2a.dat")

# Top-level -- v2b
# ################

# Stuff imported from some application module
#
# ``from simulator import *``
#
class AppConfig:
    """
    These really are class-level ("static") values.
    This is *not* a dataclass-style definition of instance variables.
    """
    table: Table
    player: Player
    samples: int
    outputfile: Path


def simulate_c(config: Union[Type[AppConfig], SimpleNamespace]) -> None:
    simulator = Simulate(config.table, config.player, config.samples)
    with Path(config.outputfile).open("w", newline="") as results:
        wtr = csv.writer(results)
        wtr.writerows(simulator)


# Configuration in the main script using a Python class definition
class Example2(AppConfig):
    dealer_rule = Hit17()
    split_rule = NoReSplitAces()
    table = Table(
        decks=6, limit=50, dealer=dealer_rule, split=split_rule, payout=(3, 2)
    )
    player_rule = SomeStrategy()
    betting_rule = Flat()
    player = Player(
        play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50
    )
    outputfile = Path.cwd() / "data" / "ch14_simulation2b.dat"
    samples = 100


if __name__ == "__main__":
    simulate_c(Example2)
    check(Path.cwd() / "data" / "ch14_simulation2b.dat")

# Top-level -- v2c
# ################

# SimpleNamespace version c
from types import SimpleNamespace

config2c = SimpleNamespace(
    dealer_rule=Hit17(),
    split_rule=NoReSplitAces(),
    player_rule=SomeStrategy(),
    betting_rule=Flat(),
    outputfile=Path.cwd() / "data" / "ch14_simulation2c.dat",
    samples=100,
)

config2c.table = Table(
    decks=6,
    limit=50,
    dealer=config2c.dealer_rule,
    split=config2c.split_rule,
    payout=(3, 2),
)
config2c.player = Player(
    play=config2c.player_rule,
    betting=config2c.betting_rule,
    max_rounds=100,
    init_stake=50,
)

if __name__ == "__main__":
    simulate_c(config2c)
    check(Path.cwd() / "data" / "ch14_simulation2c.dat")

# SimpleNamespace version 2d
# ##########################

config2d = SimpleNamespace()
config2d.dealer_rule = Hit17()
config2d.split_rule = NoReSplitAces()
config2d.table = Table(
    decks=6,
    limit=50,
    dealer=config2d.dealer_rule,
    split=config2d.split_rule,
    payout=(3, 2),
)
config2d.player_rule = SomeStrategy()
config2d.betting_rule = Flat()
config2d.player = Player(
    play=config2d.player_rule,
    betting=config2d.betting_rule,
    max_rounds=100,
    init_stake=50,
)
config2d.outputfile = Path.cwd() / "data" / "ch14_simulation2d.dat"
config2d.samples = 100

if __name__ == "__main__":
    simulate_c(config2d)
    check(Path.cwd() / "data" / "ch14_simulation2d.dat")

# SimpleNamespace version 2e
# ##########################


def make_config(
    dealer_rule: DealerRule = Hit17(),
    split_rule: SplitRule = NoReSplitAces(),
    decks: int = 6,
    limit: int = 50,
    payout: Tuple[int, int] = (3, 2),
    player_rule: PlayerStrategy = SomeStrategy(),
    betting_rule: BettingStrategy = Flat(),
    base_name: str = "ch14_simulation2e.dat",
    samples: int = 100,
) -> SimpleNamespace:
    return SimpleNamespace(
        dealer_rule=dealer_rule,
        split_rule=split_rule,
        table=Table(
            decks=decks,
            limit=limit,
            dealer=dealer_rule,
            split=split_rule,
            payout=payout,
        ),
        payer_rule=player_rule,
        betting_rule=betting_rule,
        player=Player(
            play=player_rule, betting=betting_rule, max_rounds=100, init_stake=50
        ),
        outputfile=Path.cwd() / "data" / base_name,
        samples=samples,
    )


if __name__ == "__main__":
    simulate_c(make_config(base_name="ch14_simulation2e_1.dat"))
    check(Path.cwd() / "data" / "ch14_simulation2e_1.dat")
    simulate_c(make_config(dealer_rule=Stand17(), base_name="ch14_simulation2e_2.dat"))
    check(Path.cwd() / "data" / "ch14_simulation2e_2.dat")

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
