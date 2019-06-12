#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 3. Pickle
"""

# Persistence Classes
# ========================================

import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from Chapter_10.ch10_ex1 import Post, Blog, travel, rst_render
from Chapter_10.ch10_ex2 import FaceCard, AceCard, Card, Suit

# Pickle
# ===================

# Example 1: Working
# ####################

# Use pickle to persist our microblog
import pickle
from pathlib import Path

test_pickle = """
    >>> with (Path.cwd()/"data"/"ch10_travel_blog.p").open("wb") as target:
    ...     pickle.dump(travel, target)

    >>> with(Path.cwd()/"data"/"ch10_travel_blog.p").open("rb") as source:
    ...     copy = pickle.load(source)

    >>> print(copy.title)
    Travel
    >>> for post in copy.entries:
    ...     print(post)
    Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW'])
    Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including < & > characters.', tags=['#RedRanger', '#Whitby42', '#Mistakes'])
"""

# Example 2: Won't Init
# ########################

import logging, sys

audit_log = logging.getLogger("audit")

class Hand_bad:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)
        for c in self.cards:
            audit_log.info("Initial %s", c)

    def append(self, card: Card) -> None:
        self.cards.append(card)
        audit_log.info("Hit %s", card)

    def __str__(self) -> str:
        cards = ", ".join(map(str, self.cards))
        return f"{self.dealer_card} | {cards}"


test_audit = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    >>> logging.info("bad create")
    >>> h = Hand_bad(FaceCard("K", Suit.Diamonds), AceCard("A", Suit.Clubs), Card("9", Suit.Hearts))
    >>> print(h)
    K♦ | A♣, 9♥

    >>> b = pickle.dumps(h)

    >>> logging.info("bad load from pickle")
    >>> h2 = pickle.loads(b)
    >>> print(h2)
    K♦ | A♣, 9♥
    
    >>> logging.shutdown()
"""


class Hand2:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)
        for c in self.cards:
            audit_log.info("Initial %s", c)

    def append(self, card: Card) -> None:
        self.cards.append(card)
        audit_log.info("Hit %s", card)

    def __str__(self) -> str:
        cards = ", ".join(map(str, self.cards))
        return f"{self.dealer_card} | {cards}"

    def __getstate__(self) -> Dict[str, Any]:
        return vars(self)

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # Not very secure -- hard for mypy to detect what's going on.
        self.__dict__.update(state)
        for c in self.cards:
            audit_log.info("Initial (unpickle) %s", c)

test_audit_2 = """
    >>> logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    >>> logging.info("good create")
    >>> hp = Hand2(FaceCard("K", Suit.Diamonds), AceCard("A", Suit.Clubs), Card("9", Suit.Hearts))

    >>> data = pickle.dumps(hp)

    >>> logging.info("good load from pickle")
    >>> h2p = pickle.loads(data)
    >>> print(h2p)
    K♦ | A♣, 9♥

    >>> logging.shutdown()
"""

# Example 3: Secure Pickle
# ########################

import builtins


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module: str, name: str) -> Any:
        if module == "builtins":
            if name not in ("exec", "eval"):
                return getattr(builtins, name)
        elif module in ("__main__", "Chapter_10.ch10_ex3", "ch10_ex3"):
            # Valid module names depends on execution context.
            return globals()[name]
        # elif module in any of our application modules...
        elif module in ("Chapter_10.ch10_ex2",):
            return globals()[name]
        raise pickle.UnpicklingError(
            f"global '{module}.{name}' is forbidden"
        )


test_audit_3 = """
    >>> import io
    >>> logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    >>> hp = Hand2(FaceCard("K", Suit.Diamonds), AceCard("A", Suit.Clubs), Card("9", Suit.Hearts))

    >>> data = pickle.dumps(hp)
    >>> try:
    ...     h2s = RestrictedUnpickler(io.BytesIO(data)).load()
    ... except pickle.UnpicklingError as e:
    ...     print(e)
    >>> print(h2s)
    K♦ | A♣, 9♥
    
    Creating an unimportable pickle file requires something not in Chapter_10.ch10_ex2.
    >>> from Chapter_10.ch10_ex1 import travel
    >>> bad_data = pickle.dumps(travel)
    >>> try:
    ...     travel_copy = RestrictedUnpickler(io.BytesIO(bad_data)).load()
    ... except pickle.UnpicklingError as e:
    ...     print(e)
    global 'Chapter_10.ch10_ex1.Blog' is forbidden
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
