#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 7. Example 1.
"""

# Existing Classes
# ##############################

from pathlib import Path
from enum import Enum
from typing import (
    cast,
    Iterable,
    List,
    TypeVar,
    Dict,
    Optional,
    Iterator,
    Union,
    overload,
)
from collections.abc import MutableSequence


class Suit(str, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


# collections.namedtuple and typing.NamedTuple
# ============================================

from collections import namedtuple

BlackjackCard = namedtuple("BlackjackCard", "rank,suit,hard,soft")


from typing import NamedTuple

class BlackjackCard_T(NamedTuple):
    rank: str
    suit: Suit
    hard: int
    soft: int
    def is_ace(self) -> bool:
        return False


def card(rank: int, suit: Suit) -> BlackjackCard:
    if rank == 1:
        return BlackjackCard("A", suit, 1, 11)
    elif 2 <= rank < 11:
        return BlackjackCard(str(rank), suit, rank, rank)
    elif rank == 11:
        return BlackjackCard("J", suit, 10, 10)
    elif rank == 12:
        return BlackjackCard("Q", suit, 10, 10)
    elif rank == 13:
        return BlackjackCard("K", suit, 10, 10)
    else:
        raise ValueError(f"Invalid Rank {rank}")


def card_t(rank: int, suit: Suit) -> BlackjackCard_T:
    if rank == 1:
        return BlackjackCard_T("A", suit, 1, 11)
    elif 2 <= rank < 11:
        return BlackjackCard_T(str(rank), suit, rank, rank)
    elif rank == 11:
        return BlackjackCard_T("J", suit, 10, 10)
    elif rank == 12:
        return BlackjackCard_T("Q", suit, 10, 10)
    elif rank == 13:
        return BlackjackCard_T("K", suit, 10, 10)
    else:
        raise ValueError(f"Invalid Rank {rank}")


test_namedtuple = """
    >>> c = card(10, Suit.Spades)
    >>> print(c)
    BlackjackCard(rank='10', suit=<Suit.Spades: '♠'>, hard=10, soft=10)

    >>> c_t = card_t(10, Suit.Spades)
    >>> print(c_t)
    BlackjackCard_T(rank='10', suit=<Suit.Spades: '♠'>, hard=10, soft=10)
    >>> c_t.is_ace()
    False
"""

# This doesn't work out well. The parent class cannot be defined
# with a method.
class AceCard(BlackjackCard):
    def is_ace(self) -> bool:
        return True

class AceCard_T(BlackjackCard_T):
    def is_ace(self) -> bool:
        return True

test_subclass = """
    >>> c_1 = AceCard("A", Suit.Spades, 1, 11)
    >>> print(c_1)
    AceCard(rank='A', suit=<Suit.Spades: '♠'>, hard=1, soft=11)
    
    >>> c_1t = AceCard_T("A", Suit.Spades, 1, 11)
    >>> print(c_1t)
    AceCard_T(rank='A', suit=<Suit.Spades: '♠'>, hard=1, soft=11)
    >>> c_1t.is_ace()
    True
"""

test_immutable = """
    >>> c_1 = AceCard(1, Suit.Spades, 1, 11)
    >>> c_1.rank = 12  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_immutable[1]>", line 1, in <module>
        c_1.rank = 12  # doctest: +IGNORE_EXCEPTION_DETAIL
    AttributeError: can't set attribute
    
    >>> c_1t = AceCard_T(1, Suit.Spades, 1, 11)
    >>> c_1t.rank = 12  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_immutable[3]>", line 1, in <module>
        c_1t.rank = 12  # doctest: +IGNORE_EXCEPTION_DETAIL
    AttributeError: can't set attribute
"""

# deque
# ================================

# Example of Deck built from deque.


class Card(NamedTuple):
    rank: int
    suit: Suit


import random
from collections import deque


class MultiDeck(list):
    """A sequence of decks. Each shuffled separately.
    """

    def __init__(self, size: int = 5) -> None:
        super().__init__()
        for d in range(size):
            deck = list(
                card(r, s) for r in range(1, 14) for s in cast(Iterable[Suit], Suit)
            )
            random.shuffle(deck)
            while deck:
                super().append(deck.pop())


test_multideck = """
    >>> random.seed(9973)
    >>> d = MultiDeck()
    >>> print(d.pop(), d.pop(), d.pop())
    BlackjackCard(rank='4', suit=<Suit.Diamonds: '♦'>, hard=4, soft=4) BlackjackCard(rank='A', suit=<Suit.Diamonds: '♦'>, hard=1, soft=11) BlackjackCard(rank='J', suit=<Suit.Diamonds: '♦'>, hard=10, soft=10)
    >>> more_cards = [d.pop() for _ in range(49)]
    >>> print(d.pop(), d.pop(), d.pop())
    BlackjackCard(rank='10', suit=<Suit.Hearts: '♥'>, hard=10, soft=10) BlackjackCard(rank='3', suit=<Suit.Clubs: '♣'>, hard=3, soft=3) BlackjackCard(rank='6', suit=<Suit.Clubs: '♣'>, hard=6, soft=6)
"""

# ChainMap
# =====================

import argparse
import json
import os
import sys
from collections import ChainMap
from typing import Dict, Any


def get_options(argv: List[str] = sys.argv[1:]) -> ChainMap:
    """Four Sources: comand line, file, OS environ, defaults."""
    parser = argparse.ArgumentParser(
        description="Process some integers.")
    parser.add_argument(
        "-c", "--configuration", type=open, nargs="?")
    parser.add_argument(
        "-p", "--playerclass", type=str, nargs="?",
        default="Simple")
    cmdline = parser.parse_args(argv)

    if cmdline.configuration:
        config_file = json.load(cmdline.configuration)
        cmdline.configuration.close()
    else:
        config_file = {}

    default_path = (Path.cwd() / "Chapter_7" / "ch07_defaults.json")
    with default_path.open() as default_file:
        defaults = json.load(default_file)

    combined = ChainMap(
        vars(cmdline), config_file, os.environ, defaults)
    return combined


test_options = """
    >>> options = get_options(['-p', 'Aggressive'])
    >>> print("combined", options['playerclass'])
    combined Aggressive
    >>> print("cmdline playerclass", options.maps[0].get('playerclass', None))
    cmdline playerclass Aggressive
    >>> print("config_file playerclass", options.maps[1].get('playerclass', None))
    config_file playerclass None
    >>> print("os environ playerclass", options.maps[2].get('playerclass', None))
    os environ playerclass None
    >>> print("default playerclass", options.maps[3].get('playerclass', None))
    default playerclass Passive
"""

# OrderedDict
# ======================

# No longer necessary. A ``dict`` does this, also.

# Some Sample XML
source = """
<blog>
    <topics>
        <entry ID="UUID98765"><title>first</title><body>more words</body></entry>
        <entry ID="UUID87654"><title>second</title><body>more words</body></entry>
        <entry ID="UUID65432"><title>third</title><body>more words</body></entry>
    </topics>
    <indices>
        <bytag>
            <tag text="#sometag">
                <entry IDREF="UUID87654"/>
                <entry IDREF="UUID98765"/>
            </tag>
            <tag text="#anothertag">
                <entry IDREF="UUID98765"/>
                <entry IDREF="UUID65432"/>
            </tag>
        </bytag>
        <bylocation>
            <location text="Somewhere">
                <entry IDREF="UUID98765"/>
                <entry IDREF="UUID87654"/>
            </location>
            <location text="Somewhere Else">
                <entry IDREF="UUID98765"/>
                <entry IDREF="UUID87654"/>
            </location>
        </bylocation>
    </indices>
</blog>
"""

# Parsing
from collections import OrderedDict
import xml.etree.ElementTree as etree

test_ordered_dict = """
    >>> doc = etree.XML(source)  # Parse
    >>> 
    >>> topics = OrderedDict()  # Gather <entry> tags within <topic>
    >>> for topic in doc.findall("topics/entry"):
    ...     topics[topic.attrib['ID']] = topic

    >>> # Order of entry is preserved. Always.
    >>> for topic in topics:  # Display <title> tags within each <topic>
    ...     print(topic, topics[topic].find("title").text)
    UUID98765 first
    UUID87654 second
    UUID65432 third

    >>> # We can also lookup by a key.
    >>> for tag in doc.findall("indices/bytag/tag"):
    ...     print(tag.attrib['text'])
    ...     for e in tag.findall("entry"):
    ...         print(' ', e.attrib['IDREF'], topics[e.attrib['IDREF']].find("title").text)
    #sometag
      UUID87654 second
      UUID98765 first
    #anothertag
      UUID98765 first
      UUID65432 third
"""

# The point is to keep the topics in an ordereddict by their original positions
# in the document and also reference them by ID.
# We can reference them from other places without scrambling
# the original order.

test_dict_ordering = """
    >>> some_dict = {'zzz': 1, 'aaa': 2}
    >>> some_dict['mmm'] = 3
    >>> some_dict
    {'zzz': 1, 'aaa': 2, 'mmm': 3}
    >>> sorted(some_dict)
    ['aaa', 'mmm', 'zzz']
"""

# Defaultdict
# =====================

from collections import defaultdict
from typing import DefaultDict

messages: Dict[str, str] = defaultdict(lambda: "N/A")
messages["error1"] = "Full Error Text"
messages["other"]
messages["error2"] = "Another Error Text"

test_default_dict = """
    >>> messages_with_default = [k for k in messages if messages[k] == "N/A"]
    >>> messages_with_default
    ['other']
    >>> messages['error1']
    'Full Error Text'
    >>> messages['weird']
    'N/A'
"""

from typing import Dict, List, Tuple
def dice_examples(n: int=12, seed: Any=None) -> DefaultDict[int, List]:
    if seed:
        random.seed(seed)
    Roll = Tuple[int, int]
    outcomes: DefaultDict[int, List[Roll]] = defaultdict(list)
    for _ in range(n):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        outcomes[d1+d2].append((d1, d2))
    return outcomes

test_default_dict_2 = """
    >>> d = dice_examples(12, seed=42)
    >>> d
    defaultdict(<class 'list'>, {7: [(6, 1), (1, 6), (6, 1), (2, 5)], 5: [(3, 2)], 4: [(2, 2)], 12: [(6, 6)], 6: [(5, 1), (5, 1)], 9: [(5, 4)], 2: [(1, 1)], 3: [(1, 2)]})
"""


# Counter
# ==================

# Extension of defaultdict(int)

# A Data Source
import random


def value_iterator(count=100, seed=4000) -> Iterable[str]:
    random.seed(seed, version=1)
    for i in range(count):
        yield str(random.randint(1, 6) + random.randint(1, 6))


from collections import defaultdict

T = TypeVar("T")


def freq_ordered(values: Iterable[T]) -> Dict[int, List[T]]:
    """
    Shows ties as list of pair values with the same frequency.
    """
    frequency: Dict[T, int] = defaultdict(int)
    for p in values:
        frequency[p] += 1

    rank_by_value: Dict[int, List[T]] = defaultdict(list)
    for pair, freq in frequency.items():
        rank_by_value[freq].append(pair)
    return rank_by_value


from collections import Counter

freq_2: Dict[str, int] = Counter(value_iterator())

test_counter = """
    >>> freq_1 = freq_ordered(value_iterator())
    >>> for freq in sorted(freq_1, reverse=True):
    ...     for v in freq_1[freq]:
    ...         print(repr(v), freq)
    '7' 19
    '6' 17
    '8' 16
    '10' 10
    '4' 9
    '11' 8
    '5' 8
    '9' 5
    '3' 4
    '12' 2
    '2' 2

    >>> freq_2 = Counter(value_iterator())
    >>> for k, freq in freq_2.most_common():
    ...     print(repr(k), freq)
    '7' 19
    '6' 17
    '8' 16
    '10' 10
    '4' 9
    '11' 8
    '5' 8
    '9' 5
    '3' 4
    '12' 2
    '2' 2
"""

def bag_demo() -> None:
    """
    >>> bag_demo()
    Counter({'a': 2, 'r': 1, 'd': 1, 'w': 1, 'o': 1, 'l': 1, 'v': 1, 'e': 1, 's': 1})
    Counter({'o': 2, 'z': 1, 'y': 1, 'm': 1, 'l': 1, 'g': 1, 'i': 1, 'e': 1, 's': 1})
    Counter({'o': 3, 'a': 2, 'l': 2, 'e': 2, 's': 2, 'r': 1, 'd': 1, 'w': 1, 'v': 1, 'z': 1, 'y': 1, 'm': 1, 'g': 1, 'i': 1})
    Counter({'a': 2, 'r': 1, 'd': 1, 'w': 1, 'v': 1})
    Counter({'z': 1, 'y': 1, 'm': 1, 'o': 1, 'g': 1, 'i': 1})
    """
    bag1 = Counter("aardwolves")
    bag2 = Counter("zymologies")
    print(bag1)
    print(bag2)
    print(bag1+bag2)
    print(bag1-bag2)
    print(bag2-bag1)


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)

    # performance()
