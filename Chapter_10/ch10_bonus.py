"""
Enumerate all Blackjack outcomes with player mirroring the dealer choice.
Note that player going bust first is a loss, irrespective of what the dealer holds.

The question, then, is given two cards, what are the odds of going bust using
dealer rules of hit 17, stand on 18.

Then bust for player is rule 1.
Bust for dealer is rule 2.
Otherwise it's a 50/50 proposition.
"""
from typing import Optional, Tuple, Dict, Counter
import random
from enum import Enum
import collections

class Suit(Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"

class Card:

    def __init__(self, rank: str, suit: Suit, hard: Optional[int]=None, soft: Optional[int]=None) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard or int(rank)
        self.soft = soft or int(rank)

    def __str__(self) -> str:
        return f"{self.rank!s}{self.suit.value!s}"


class AceCard(Card):

    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard(Card):

    def __init__(self, rank: str, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)

def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif rank in (11, 12, 13):
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(rank_str, suit)
    else:
        return Card(str(rank), suit)

class Deck(list):
    def __init__(self) -> None:
        super().__init__(card(r, s) for r in range(1, 14) for s in Suit)
        random.shuffle(self)

class Hand(list):
    @property
    def hard(self) -> int:
        return sum(c.hard for c in self)

    @property
    def soft(self) -> int:
        return sum(c.soft for c in self)

    def __repr__(self) -> str:
        cards = [str(c) for c in self]
        return f"Hand({cards!r})"

def deal_rules(deck: Deck) -> Tuple[Hand, Optional[int]]:
    hand = Hand([deck.pop(), deck.pop()])
    while hand.hard < 21:
        if hand.soft == 21:
            return hand, 21
        elif hand.hard == 21:
            return hand, 21
        elif hand.soft < 18:
            hand.append(deck.pop())
        elif hand.soft > 21 and hand.hard < 18:
            hand.append(deck.pop())
        else:
            return hand, min(hand.hard, hand.soft)
    return hand, None

def simulation() -> None:
    raw_outcomes: Counter[Tuple[Optional[int], Optional[int]]] = collections.Counter()
    game_payout: Counter[str] = collections.Counter()

    for i in range(20_000):
        deck = Deck()
        player_hand, player_result = deal_rules(deck)
        dealer_hand, dealer_result = deal_rules(deck)
        raw_outcomes[(player_result, dealer_result)] += 1
        if player_result is None:
            game_payout['loss'] += 1
        elif player_result is 21:
            game_payout['21'] += 1
        elif dealer_result is None:
            game_payout['win'] += 1
        elif player_result > dealer_result:
            game_payout['win'] += 1
        elif player_result == dealer_result:
            game_payout['push'] += 1
        else:
            game_payout['loss'] += 1

    running = 0.0
    for outcome, count in game_payout.most_common():
        print(f"{running:.3f} <= r < {running+count/20_000:.3f}: {outcome}")
        running += count/20_000

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    simulation()
