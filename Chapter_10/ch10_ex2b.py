#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 2. YAML (part b)
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from Chapter_10.ch10_ex2 import Suit, Card, AceCard, FaceCard

# YAML -- 2b cards with custom representations
# =============================================

deck = [AceCard("A", Suit.Clubs), Card("2", Suit.Hearts), FaceCard("K", Suit.Diamonds)]

import yaml


def card_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!Card", f"{card.rank!s}{card.suit.value!s}")


def acecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!AceCard", f"{card.rank!s}{card.suit.value!s}")


def facecard_representer(dumper: Any, card: Card) -> str:
    return dumper.represent_scalar(
        "!FaceCard", f"{card.rank!s}{card.suit.value!s}")


def card_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return Card(rank, Suit(suit))


def acecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return AceCard(rank, Suit(suit))


def facecard_constructor(loader: Any, node: Any) -> Card:
    value = loader.construct_scalar(node)
    rank, suit = value[:-1], value[-1]
    return FaceCard(rank, Suit(suit))

# Changes to the yaml module will apply throughout the application.
# And this test run, also.
# We can also add this

yaml.add_representer(Card, card_representer)
yaml.add_representer(AceCard, acecard_representer)
yaml.add_representer(FaceCard, facecard_representer)
yaml.add_constructor("!Card", card_constructor)
yaml.add_constructor("!AceCard", acecard_constructor)
yaml.add_constructor("!FaceCard", facecard_constructor)

test_yaml_dump_load = """
    >>> print(*map(str, deck))
    A♣ 2♥ K♦
    
    >>> text = yaml.dump(deck, allow_unicode=True)
    >>> print(text)
    - !AceCard 'A♣'
    - !Card '2♥'
    - !FaceCard 'K♦'
    <BLANKLINE>
    
    >>> copy = yaml.load(text, Loader=yaml.Loader)
    >>> print(*map(str, copy))
    A♣ 2♥ K♦
"""


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
