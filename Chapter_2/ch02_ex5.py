#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 2. Example 5.
"""

# Alternative Designs for the Initialization

from Chapter_2.ch02_ex3 import Card, card, Suit
from typing import List, Iterable, cast, Union, NamedTuple, Tuple, Optional, overload

import random

# While Card should be immutable, that's a topic for the next chapter.

# Composite Objects: Deck
# ====================================

# A simple Deck definition

test_no_deck = """
    >>> random.seed(42)
    >>> d = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
    >>> random.shuffle(d)
    >>> hand = [d.pop(), d.pop()]
    >>> hand
    [FaceCard(suit=<Suit.Club: '♣'>, rank='J'), Card(suit=<Suit.Spade: '♠'>, rank='2')]
"""


class Deck:

    def __init__(self) -> None:
        self._cards = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        return self._cards.pop()


test_deck = """
    >>> random.seed(42)
    >>> d = Deck()
    >>> hand = [d.pop(), d.pop()]
    >>> hand
    [FaceCard(suit=<Suit.Club: '♣'>, rank='J'), Card(suit=<Suit.Spade: '♠'>, rank='2')]
"""


# A subclass of list definition


class Deck2(list):

    def __init__(self) -> None:
        super().__init__(
            card(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit)
        )
        random.shuffle(self)


test_deck2 = """
    >>> random.seed(42)
    >>> d = Deck2()
    >>> hand = [d.pop(), d.pop()]
    >>> hand
    [FaceCard(suit=<Suit.Club: '♣'>, rank='J'), Card(suit=<Suit.Spade: '♠'>, rank='2')]
"""


# A better subclass of list which has the necessary additional features of
# multiple sets of cards plus not dealing the entire deck.


class Deck3(list):

    def __init__(self, decks: int = 1) -> None:
        super().__init__()
        for i in range(decks):
            self.extend(card(r + 1, s) for r in range(13) for s in iter(Suit))
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


test_deck3 = """
    >>> random.seed(42)
    >>> d = Deck3()
    >>> hand = [d.pop(), d.pop()]
    >>> hand
    [Card(suit=<Suit.Spade: '♠'>, rank='9'), FaceCard(suit=<Suit.Heart: '♥'>, rank='K')]
"""


class Deck3a(list):

    def __init__(self, decks: int = 1) -> None:
        super().__init__(
            card(r + 1, s) for r in range(13) for s in iter(Suit) for d in range(decks)
        )
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


test_deck3a = """
    >>> random.seed(42)
    >>> d = Deck3a()
    >>> hand = [d.pop(), d.pop()]
    >>> hand
    [Card(suit=<Suit.Spade: '♠'>, rank='9'), FaceCard(suit=<Suit.Heart: '♥'>, rank='K')]
"""


# Composite Objects: Hand
# ===================================

# A simplistic Hand without a proper initialization of the cards.


class Hand:

    def __init__(self, dealer_card: Card) -> None:
        self.dealer_card: Card = dealer_card
        self.cards: List[Card] = []

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.dealer_card} {self.cards}"


test_hand = """
    >>> random.seed(42)
    >>> d = Deck()
    >>> h = Hand(d.pop())
    >>> h.cards.append(d.pop())
    >>> h.cards.append(d.pop())
    >>> h
    Hand J♣ [Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')]
"""


# A Better Hand with a complete initialization of the cards.
# This works better with serialization.


class Hand2:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def card_append(self, card: Card) -> None:
        self.cards.append(card)

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dealer_card!r}, *{self.cards})"


test_hand2 = """
    >>> random.seed(42)
    >>> d = Deck()
    >>> h = Hand2(d.pop(), d.pop(), d.pop())
    >>> h
    Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])"""


# A Hand which can be built from another Hand or a collection of Cards.
# This allows us to freeze the hand or build a memento version of the hand.


class Hand3:

    @overload
    def __init__(self, arg1: "Hand3") -> None:
        ...

    @overload
    def __init__(self, arg1: Card, arg2: Card, arg3: Card) -> None:
        ...

    def __init__(
        self,
        arg1: Union[Card, "Hand3"],
        arg2: Optional[Card] = None,
        arg3: Optional[Card] = None,
    ) -> None:
        self.dealer_card: Card
        self.cards: List[Card]

        if isinstance(arg1, Hand3) and not arg2 and not arg3:
            # Clone an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif (
            isinstance(arg1, Card) and isinstance(arg2, Card) and isinstance(arg3, Card)
        ):
            # Build a fresh, new hand.
            self.dealer_card = cast(Card, arg1)
            self.cards = [arg2, arg3]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dealer_card!r}, *{self.cards})"


test_hand3 = """
    >>> random.seed(42)
    >>> d = Deck()
    >>> h = Hand3(d.pop(), d.pop(), d.pop())
    >>> memento = Hand3(h)
    >>> memento
    Hand3(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
"""

# A Hand which can be built from another Hand.
# Or a split from another hand.
# Or individual cards.

# Note the complexity of the initialization is nearly impossible
# to specify clearly.
# - __init__(self, arg1 : Hand4) -> None: ...
# - __init__(self, arg1 : Hand4, arg2: Card, *, split: int) -> None: ...
# - __init__(self, arg1 : Card, arg2: Card, arg3: Card) -> None: ...
# - __init__(self, arg1 : Union[Hand4, Card], arg2: Optional[Card]=None, arg3: Optional[Card] = None, split: Optional[int] = None) -> None: ...

# This is an indication of a need to have staticmethods for creating instances.
# See the next example for this.


class Hand4:

    @overload
    def __init__(self, arg1: "Hand4") -> None:
        ...

    @overload
    def __init__(self, arg1: "Hand4", arg2: Card, *, split: int) -> None:
        ...

    @overload
    def __init__(self, arg1: Card, arg2: Card, arg3: Card) -> None:
        ...

    def __init__(
        self,
        arg1: Union["Hand4", Card],
        arg2: Optional[Card] = None,
        arg3: Optional[Card] = None,
        split: Optional[int] = None,
    ) -> None:
        self.dealer_card: Card
        self.cards: List[Card]
        if isinstance(arg1, Hand4):
            # Clone an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif isinstance(arg1, Hand4) and isinstance(arg2, Card) and "split" is not None:
            # Split an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = [arg1.cards[split], arg2]
        elif isinstance(arg1, Card) and isinstance(arg2, Card) and isinstance(
            arg3, Card
        ):
            # Build a fresh, new hand from three cards
            self.dealer_card = arg1
            self.cards = [arg2, arg3]
        else:
            raise TypeError("Invalid constructor {arg1!r} {arg2!r} {arg3!r}")

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))


test_hand4 = """
    >>> import random
    >>> random.seed(42)
    >>> d = Deck()
    >>> h = Hand4(d.pop(), d.pop(), d.pop())
    >>> s1 = Hand4(h, d.pop(), split=0)
    >>> s2 = Hand4(h, d.pop(), split=1)
    >>> print("start", h, "split1", s1, "split2", s2)
    start 2♠, A♦ split1 2♠, A♦ split2 2♠, A♦
"""

# A Hand with static methods to split or frozen as a memento.


class Hand5:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    @staticmethod
    def freeze(other) -> "Hand5":
        hand = Hand5(other.dealer_card, *other.cards)
        return hand

    @staticmethod
    def split(other, card0, card1) -> Tuple["Hand5", "Hand5"]:
        hand0 = Hand5(other.dealer_card, other.cards[0], card0)
        hand1 = Hand5(other.dealer_card, other.cards[1], card1)
        return hand0, hand1

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))


test_hand_5 = """
    >>> import random
    >>> random.seed(42)
    >>> d = Deck()
    >>> h = Hand5(d.pop(), d.pop(), d.pop())
    >>> s1, s2 = Hand5.split(h, d.pop(), d.pop())
    >>> print("start", h, "split1", s1, "split2", s2)
    start 2♠, A♦ split1 2♠, Q♠ split2 A♦, 5♦
"""

# Composite Objects: Betting Strategy
# ==============================================

# A strategy class hierarchy for Betting.


class BettingStrategy:

    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class Flat(BettingStrategy):

    def bet(self) -> int:
        return 1


test_flat = """
    >>> flat_bet = Flat()
    >>> flat_bet.bet()
    1
"""

import abc
from abc import abstractmethod


class BettingStrategy2(metaclass=abc.ABCMeta):

    @abstractmethod
    def bet(self) -> int:
        return 1

    def record_win(self):
        pass

    def record_loss(self):
        pass


# A strategy class hierarchy for Play.


class GameStrategy:

    def insurance(self, hand: Hand) -> bool:
        return False

    def split(self, hand: Hand) -> bool:
        return False

    def double(self, hand: Hand) -> bool:
        return False

    def hit(self, hand: Hand) -> bool:
        return sum(c.hard for c in hand.cards) <= 17


test_game = """
    >>> dumb = GameStrategy()
    >>> dumb.insurance(Hand2(card(1, Suit.Heart), card(1, Suit.Spade), card(13, Suit.Spade)))
    False
    >>> h17 = Hand2(card(1, Suit.Heart), card(10, Suit.Heart), card(7, Suit.Club))
    >>> [f"{c}: {c.hard}" for c in h17.cards]
    ['10♥: 10', '7♣: 7']
    >>> [f"{c}: {c.soft}" for c in h17.cards]
    ['10♥: 10', '7♣: 7']
    >>> dumb.hit(Hand2(card(1, Suit.Heart), card(10, Suit.Heart), card(7, Suit.Club)))
    True
    >>> dumb.hit(Hand2(card(1, Suit.Heart), card(10, Suit.Heart), card(8, Suit.Club)))
    False
    >>> s18 = Hand2(card(1, Suit.Heart), card(1, Suit.Heart), card(7, Suit.Club))
    >>> [f"{c}: {c.hard}" for c in s18.cards]
    ['A♥: 1', '7♣: 7']
    >>> [f"{c}: {c.soft}" for c in s18.cards]
    ['A♥: 11', '7♣: 7']
"""


# A simple outline for the Table.


class Table:

    def __init__(self) -> None:
        self.deck = Deck()

    def place_bet(self, amount: int) -> None:
        print("Bet", amount)

    def get_hand(self) -> Hand2:
        try:
            self.hand = Hand2(self.deck.pop(), self.deck.pop(), self.deck.pop())
            self.hole_card = self.deck.pop()
        except IndexError:
            # Out of cards: need to shuffle.
            # This is not technically correct: cards currently in play should not appear in the next deck.
            self.deck = Deck()
            return self.get_hand()
        print("Deal", self.hand)
        return self.hand

    def can_insure(self, hand: Hand) -> bool:
        return hand.dealer_card.insure


# A Player definition


class Player:

    def __init__(
        self,
        table: Table,
        bet_strategy: BettingStrategy,
        game_strategy: GameStrategy
    ) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure(self.bet_strategy.bet())
        # etc.


# Typical Use Case

test_table_player = """
    >>> random.seed(42)
    >>> table = Table()
    >>> flat_bet = Flat()
    >>> dumb = GameStrategy()
    >>> p = Player(table, flat_bet, dumb)
    >>> p.game()
    Bet 1
    Deal Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
"""

# A Player definition using wide-open keyword definitions.
# While the following is *technically* possible, a Very Bad Idea for type checking.
#         self.__dict__.update(kw)


class Player2(Player):

    def __init__(self, **kw) -> None:
        """Must provide table, bet_strategy, game_strategy."""
        self.bet_strategy: BettingStrategy = kw["bet_strategy"]
        self.game_strategy: GameStrategy = kw["game_strategy"]
        self.table: Table = kw["table"]
        self.log_name: Optional[str] = kw.get("log_name")

    def game(self) -> None:
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()


# Typical Use Case.


test_table_player2 = """
    >>> random.seed(42)
    >>> table = Table()
    >>> flat_bet = Flat()
    >>> dumb = GameStrategy()
    >>> p2 = Player2(table=table, bet_strategy=flat_bet, game_strategy=dumb)
    >>> p2.game()
    Bet 1
    Deal Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
"""

class Player2x(Player):

    def __init__(self, **kw) -> None:
        """Must provide table, bet_strategy, game_strategy."""
        self.bet_strategy: BettingStrategy = kw["bet_strategy"]
        self.game_strategy: GameStrategy = kw["game_strategy"]
        self.table: Table = kw["table"]
        self.log_name: Optional[str] = kw.get("log_name")

    def game(self) -> None:
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()


# Bonus Use Case. Set an additional attribute.

test_table_player2_extra = """
    >>> random.seed(42)
    >>> table = Table()
    >>> flat_bet = Flat()
    >>> dumb = GameStrategy()
    >>> p2 = Player2x(table=table, bet_strategy=flat_bet, game_strategy=dumb, log_name="Flat/Dumb")
    >>> p2.game()
    Bet 1
    Deal Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
    >>> print(p2.log_name, p2.hand)
    Flat/Dumb Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
"""


# A Player definition using wide-open keyword definitions.
# While ``self.__dict__.update(extras)`` is *technically* possible, it's a bad idea.


class Player3(Player):

    def __init__(
        self,
        table: Table,
        bet_strategy: BettingStrategy,
        game_strategy: GameStrategy,
        **extras,
    ) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table
        # Bad: self.__dict__.update(extras)
        # Slightly better?
        for name in extras:
            setattr(self, name, extras[name])
        # Much Better
        self.log_name: str = extras.pop("log_name", self.__class__.__name__)
        if extras:
            raise TypeError(f"Extra **kw arguments: {extras!r}")


test_table_player3 = """
    >>> random.seed(42)
    >>> table = Table()
    >>> flat_bet = Flat()
    >>> dumb = GameStrategy()
    >>> p3 = Player3(table, flat_bet, dumb, log_name="Flat/Dumb")
    >>> p3.game()
    Bet 1
    Deal Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
    >>> print(p3.log_name, p3.hand)
    Flat/Dumb Hand2(FaceCard(suit=<Suit.Club: '♣'>, rank='J'), *[Card(suit=<Suit.Spade: '♠'>, rank='2'), AceCard(suit=<Suit.Diamond: '♦'>, rank='A')])
"""

# Bad Ideas
# ====================

# class-level Validation
#
# Run-time complexity for little real value. These are design issues. Use mypy and do it only once.


class ValidPlayer:

    def __init__(self, table, bet_strategy, game_strategy):
        assert isinstance(table, Table)
        assert isinstance(bet_strategy, BettingStrategy)
        assert isinstance(game_strategy, GameStrategy)

        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table


test_table_valid_player = """
    >>> import random
    >>> random.seed(42)
    >>> table = Table()
    >>> flat_bet = Flat()
    >>> dumb = GameStrategy()
    >>> p4 = ValidPlayer(table, flat_bet, dumb)
"""


class Player4:

    def __init__(
        self, table: Table, bet_strategy: BettingStrategy, game_strategy: GameStrategy
    ) -> None:
        """Creates a new player associated with a table, and configured with
        proper betting and play strategies

        :param table: an instance of :class:`Table`
        :param bet_strategy: an instance of :class:`BettingStrategy`
        :param game_strategy: an instance of :class:`GameStrategy`
        """
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
