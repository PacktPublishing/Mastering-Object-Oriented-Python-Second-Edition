#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 2. YAML (part c)
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from Chapter_10.ch10_ex2 import Suit, Card, AceCard, FaceCard
from Chapter_10.ch10_ex2b import facecard_representer, acecard_representer, card_representer

# YAML -- 2c cards with safe custom representations
# ==================================================

import yaml


class Card2(yaml.YAMLObject):
    yaml_tag = "!Card2"
    yaml_loader = yaml.SafeLoader

    def __init__(self, rank, suit, hard=None, soft=None) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard or int(rank)
        self.soft = soft or int(rank)

    def __str__(self) -> str:
        return "{0.rank!s}{0.suit!s}".format(self)


class AceCard2(Card2):
    yaml_tag = "!AceCard2"

    def __init__(self, rank, suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard2(Card2):
    yaml_tag = "!FaceCard2"

    def __init__(self, rank, suit) -> None:
        super().__init__(rank, suit, 10, 10)


deck2 = [AceCard2("A", "♣"), Card2("2", "♥"), FaceCard2("K", "♦")]

test_yaml_dump_safe_load = """
    # Changes to the yaml module will apply throughout the application.
    >>> yaml.add_representer(Card, card_representer)
    >>> yaml.add_representer(AceCard, acecard_representer)
    >>> yaml.add_representer(FaceCard, facecard_representer)

    >>> text2 = yaml.dump(deck2)
    >>> print(text2)
    - !AceCard2
      hard: 1
      rank: A
      soft: 11
      suit: "\\u2663"
    - !Card2
      hard: 2
      rank: '2'
      soft: 2
      suit: "\\u2665"
    - !FaceCard2
      hard: 10
      rank: K
      soft: 10
      suit: "\\u2666"
    <BLANKLINE>
    
    >>> copy = yaml.safe_load(text2)
    >>> print([str(c) for c in copy])
    ['A♣', '2♥', 'K♦']
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
