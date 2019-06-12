#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 2. YAML (part a)
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from Chapter_10.ch10_ex1 import Post, Blog, travel, rst_render
from Chapter_10.ch10_ex2 import Suit, Card, FaceCard, AceCard

# YAML
# ===================

import yaml

# Example 1: That's it.
# ######################

# Start with original definitions

test_yaml = """
    >>> text = yaml.dump(travel)
    >>> print(text)
    !!python/object:Chapter_10.ch10_ex1.Blog
    entries:
    - !!python/object:Chapter_10.ch10_ex1.Post
      date: 2013-11-14 17:25:00
      rst_text: "Some embarrassing revelation. Including \\u2639 and \\u2693\\uFE0E"
      tags:
      - '#RedRanger'
      - '#Whitby42'
      - '#ICW'
      title: Hard Aground
    - !!python/object:Chapter_10.ch10_ex1.Post
      date: 2013-11-18 15:30:00
      rst_text: Some witty epigram. Including < & > characters.
      tags:
      - '#RedRanger'
      - '#Whitby42'
      - '#Mistakes'
      title: Anchor Follies
    title: Travel
    <BLANKLINE>
    
    >>> copy = yaml.load(text)
    >>> print(type(copy), copy.title)
    <class 'Chapter_10.ch10_ex1.Blog'> Travel
    >>> for p in copy.entries:
    ...        print(p.date.year, p.date.month, p.date.day, p.title, p.tags)
    2013 11 14 Hard Aground ['#RedRanger', '#Whitby42', '#ICW']
    2013 11 18 Anchor Follies ['#RedRanger', '#Whitby42', '#Mistakes']

    >>> text2 = yaml.dump(travel, allow_unicode=True)
    >>> print(text2)
    !!python/object:Chapter_10.ch10_ex1.Blog
    entries:
    - !!python/object:Chapter_10.ch10_ex1.Post
      date: 2013-11-14 17:25:00
      rst_text: Some embarrassing revelation. Including ☹ and ⚓︎
      tags:
      - '#RedRanger'
      - '#Whitby42'
      - '#ICW'
      title: Hard Aground
    - !!python/object:Chapter_10.ch10_ex1.Post
      date: 2013-11-18 15:30:00
      rst_text: Some witty epigram. Including < & > characters.
      tags:
      - '#RedRanger'
      - '#Whitby42'
      - '#Mistakes'
      title: Anchor Follies
    title: Travel
    <BLANKLINE>

"""

with (Path.cwd()/"data"/"ch10.yaml").open("w", encoding="UTF-8") as target:
    yaml.dump(travel, target)

# Example 2: Cards
# ###################


deck = [AceCard("A", Suit.Clubs), Card("2", Suit.Hearts), FaceCard("K", Suit.Diamonds)]

test_yaml_dump = """
    >>> text = yaml.dump(deck, allow_unicode=True)
    >>> print(text)
    - !!python/object:Chapter_10.ch10_ex2.AceCard
      hard: 1
      rank: A
      soft: 11
      suit: !!python/object/apply:Chapter_10.ch10_ex2.Suit
      - ♣
    - !!python/object:Chapter_10.ch10_ex2.Card
      hard: 2
      rank: '2'
      soft: 2
      suit: !!python/object/apply:Chapter_10.ch10_ex2.Suit
      - ♥
    - !!python/object:Chapter_10.ch10_ex2.FaceCard
      hard: 10
      rank: K
      soft: 10
      suit: !!python/object/apply:Chapter_10.ch10_ex2.Suit
      - ♦
    <BLANKLINE>    
"""


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
