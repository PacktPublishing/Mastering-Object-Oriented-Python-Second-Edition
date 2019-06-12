#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 1 -- simulation model.
"""

from dataclasses import dataclass, astuple, asdict, field
from typing import Tuple, Iterator
from pathlib import Path
import csv

# Mock Object Model
# =====================

# A set of class hierarchies that we'll use for several examples.
# The content is mostly mocks.
class DealerRule:

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

class Hit17(DealerRule):
    """Hits soft 17"""
    pass


class Stand17(DealerRule):
    """Stands on soft 17"""
    pass


class SplitRule:

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class ReSplit(SplitRule):
    """Simplistic resplit anything."""
    pass


class NoReSplit(SplitRule):
    """Simplistic no resplit."""
    pass


class NoReSplitAces(SplitRule):
    """One card only to aces; no resplit."""
    pass


@dataclass
class Table:

    decks: int
    limit: int
    dealer: DealerRule
    split: SplitRule
    payout: Tuple[int, int]


class PlayerStrategy:

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class SomeStrategy(PlayerStrategy):
    pass


class AnotherStrategy(PlayerStrategy):
    pass


class BettingStrategy:

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class Flat(BettingStrategy):
    pass


class Martingale(BettingStrategy):
    pass


class OneThreeTwoSix(BettingStrategy):
    pass


@dataclass
class Player:

    play: PlayerStrategy
    betting: BettingStrategy
    max_rounds: int
    init_stake: int

    rounds: int = field(init=False)
    stake: float = field(init=False)

    def __post_init__(self):
        self.reset()

    def reset(self) -> None:
        self.rounds = self.max_rounds
        self.stake = self.init_stake


# A mock simulation which is built from the above mock objects.
import random


@dataclass
class Simulate:
    """Mock simulation."""

    table: Table
    player: Player
    samples: int

    def __iter__(self) -> Iterator[Tuple]:
        """Yield statistical samples."""
        x, y = self.table.payout
        blackjack_payout = x / y
        for count in range(self.samples):
            self.player.reset()
            while self.player.stake > 0 and self.player.rounds > 0:
                self.player.rounds -= 1

                outcome = random.random()
                if outcome < 0.579:
                    self.player.stake -= 1
                elif 0.579 <= outcome < 0.883:
                    self.player.stake += 1
                elif 0.883 <= outcome < 0.943:
                    # a "push"
                    pass
                else:
                    # 0.943 <= outcome
                    self.player.stake += blackjack_payout

            yield astuple(self.table) + astuple(self.player)


def check(path: Path) -> None:
    """
    Validate unit test result file can be read.

    :param path: Path to the example output
    """
    with path.open("r") as results:
        rdr = csv.reader(results)
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
            f"{path}\nMean = {mean:.1f}\n"
            f"House Edge = { 1 - mean / 50:.1%}\n"
            f"Range = {value_min:.1f} {value_max:.1f}"
        )
