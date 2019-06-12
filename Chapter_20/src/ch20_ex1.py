#!/usr/bin/env python3.7
# Mastering Object-Oriented Python 2e
#
# Code Examples for Mastering Object-Oriented Python 2nd Edition
#
# Chapter 20. Example 1.
#
"""
Blackjack Cards and Decks
=========================

This module contains a definition of :class:`Card`, 
:class:`Deck` and :class:`Shoe` suitable for Blackjack.

The :class:`Card` class hierarchy
---------------------------------

The :class:`Card` class hierarchy includes the following class definitions.

:class:`Card` is the superclass as well as being the class for number cards.
:class:`FaceCard` defines face cards: J, Q and K.
:class:`AceCard` defines the Ace. This is special in Blackjack because it creates a soft total for a hand.

We create cards using the :func:`card` factory function to create the proper
:class:`Card` subclass instances from a rank and suit.

The :class:`Suit` enumeration has all of the Suit instances.

::

    >>> from ch20_ex1 import cards
    >>> ace_clubs= cards.card( 1, cards.suits[0] )
    >>> ace_clubs
    'A♣'
    >>> ace_diamonds= cards.card( 1, cards.suits[1] )
    >>> ace_clubs.rank ==  ace_diamonds.rank
    True

The :class:`Deck` and :class:`Shoe` class hierarchy
---------------------------------------------------

The basic :class:`Deck` creates a single 52-card deck. The :class:`Shoe` subclass creates a given number of decks. A :class:`Deck`
can be shuffled before the cards can be extracted with the :meth:`pop` method. A :class:`Shoe` must be shuffled and
*burned*. The burn operation sequesters a random number of cards based on a mean and standard deviation. The mean is
a number of cards (52 is the default.) The standard deviation for the burn is also given as a number of cards (2 is
the default.)

"""

# Example Sphinx-style Documentation
# -------------------------------------

# Imports
from enum import Enum
from typing import Optional


class Suit(str, Enum):
    """
    Enumeration of all possible values for a card's suit.
    """
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card:
    """
    Definition of a numeric rank playing card.
    Subclasses will define :py:class:`FaceCard` and :py:class:`AceCard`.

    :ivar rank: int rank of the card
    :ivar suit: Suit suit of the card
    :ivar hard: int Hard point total for a card
    :ivar soft: int Soft total; same as hard for all cards except Aces.
    """

    def __init__(
        self, rank: int, suit: Suit, hard: int, soft: Optional[int] = None
    ) -> None:
        """Define the values for this card.

        :param rank: Numeric rank in the range 1-13.
        :param suit: Suit object (often a character from '♣♡♢♠')
        :param hard: Hard point total (or 10 for FaceCard or 1 for AceCard)
        :param soft: The soft total for AceCard, otherwise defaults to hard.
        """
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft if soft is not None else hard

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit})"


class FaceCard(Card):
    """
    Subclass of :py:class:`Card` with Ranks 11-13 represented by J, Q, and K.
    """
    rank_str = {11: "J", 12: "Q", 13: "K"}

    def __str__(self) -> str:
        return f"{self.rank_str[self.rank]}{self.suit}"


class AceCard(Card):
    """
    Subclass of :py:class:`Card` with rank of 1 represented by A.
    """

    def __str__(self) -> str:
        return f"A{self.suit}"


def card(rank: int, suit: Suit) -> Card:
    """
    Create a :py:class:`Card` instance from rank and suit.
    Can raise :py:exc:`TypeError` for ranks out of the range 1 to 13, inclusive.

    :param suit: Suit object
    :param rank: Numeric rank in the range 1-13
    :returns: :py:class:`Card` instance
    :raises TypeError: rank out of range
c
    >>> from Chapter_20.ch20_ex1 import card
    >>> str(card(3, Suit.Heart))
    '3♥'
    >>> str(card(1, Suit.Heart))
    'A♥'
    """
    if rank == 1:
        return AceCard(rank, suit, 1, 11)
    elif 2 <= rank < 11:
        return Card(rank, suit, rank)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit, 10)
    else:
        raise TypeError
