#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 5 -- simulation model.
"""

from typing import Tuple, Iterator

# Mock Object Model
# =====================

# A set of class hierarchies that we'll use for several examples.
# The content is mostly mocks.
class DealerRule:
    pass


class Hit17(DealerRule):
    """Hits soft 17"""
    pass


class Stand17(DealerRule):
    """Stands on soft 17"""
    pass


class SplitRule:
    pass


class ReSplit(SplitRule):
    """Simplistic resplit anything."""
    pass


class NoReSplit(SplitRule):
    """Simplistic no resplit."""
    pass


class NoReSplitAces(SplitRule):
    """One card only to aces; no resplit."""
    pass


class Table:

    def __init__(self, decks: int, limit: int, dealer: DealerRule, split: SplitRule, payout: Tuple[int, int]) -> None:
        self.decks = decks
        self.limit = limit
        self.dealer = dealer
        self.split = split
        self.payout = payout

    def as_tuple(self):
        return (
            self.decks,
            self.limit,
            self.dealer.__class__.__name__,
            self.split.__class__.__name__,
            self.payout,
        )


class PlayerStrategy:
    pass


class SomeStrategy(PlayerStrategy):
    pass


class AnotherStrategy(PlayerStrategy):
    pass


class BettingStrategy:

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


class Player:

    def __init__(self, play: PlayerStrategy, betting: BettingStrategy, rounds: int, stake: int) -> None:
        self.play = play
        self.betting = betting
        self.max_rounds = rounds
        self.init_stake = float(stake)

    def reset(self) -> None:
        self.rounds = self.max_rounds
        self.stake = self.init_stake

    def as_tuple(self) -> Tuple:
        return (
            self.play.__class__.__name__,
            self.betting.__class__.__name__,
            self.max_rounds,
            self.init_stake,
            self.rounds,
            self.stake,
        )


# A mock simulation which is built from the above mock objects.
import random


class Simulate:

    def __init__(
            self,
            table: Table,
            player: Player,
            samples: int
    ) -> None:
        """Define table, player and number of samples."""
        self.table = table
        self.player = player
        self.samples = samples

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

            yield self.table.as_tuple() + self.player.as_tuple()
