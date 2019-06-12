#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 6. Example 2.
"""
from typing import Callable, TypeVar, Iterable, Iterator, cast, Dict, Match
from pathlib import Path

# Contexts
# =================

# With statement example 1 -- file processing

def slow(source="itmaybeahack.com.bkup-Feb-2012.gz") -> int:
    from pathlib import Path
    source_path = Path.cwd()/"data"/source
    target_path = Path.cwd()/"data"/"subset.csv"

    import re

    format_1_pat = re.compile(
        r"([\d\.]+)\s+"  # digits and .'s: host
        r"(\S+)\s+"  # non-space: logname
        r"(\S+)\s+"  # non-space: user
        r"\[(.+?)\]\s+"  # Everything in []: time
        r'"(.+?)"\s+'  # Everything in "": request
        r"(\d+)\s+"  # digits: status
        r"(\S+)\s+"  # non-space: bytes
        r'"(.*?)"\s+'  # Everything in "": referrer
        r'"(.*?)"\s*'  # Everything in "": user agent
    )
    import gzip
    import csv

    T = Optional[Match[str]]
    class Counter:
        def __init__(self, source: Iterable[T]) -> None:
            self.source_iter = source
            self.count = 0
        def __iter__(self) -> Iterator[T]:
            for item in self.source_iter:
                yield item
                self.count += 1

    with target_path.open('w', newline='') as target:
        wtr = csv.writer(target)
        with gzip.open(source_path, "r") as source:
            line_iter = (b.decode() for b in source)
            row_iter = Counter(format_1_pat.match(line) for line in line_iter)
            non_empty_rows: Iterator[Match] = filter(None, row_iter)
            wtr.writerows(m.groups() for m in non_empty_rows)
    return row_iter.count

test_file_proc = """
    >>> import time
    >>> start = time.perf_counter()
    >>> rows = slow()
    >>> end = time.perf_counter()    
    >>> print(f"Wrote {rows:,} summary rows in {end-start:.3f} seconds")  # doctest: +ELLIPSIS
    Wrote 380,517 summary rows in ... seconds
"""

# With statement example 2 -- decimal contexts

test_decimal = """
    >>> import decimal

    >>> PENNY = decimal.Decimal("0.00")
    >>> price = decimal.Decimal("15.99")
    >>> rate = decimal.Decimal("0.0075")
    >>> print(f"Tax={(price * rate).quantize(PENNY)}, Fully={price * rate}")
    Tax=0.12, Fully=0.119925
    >>> with decimal.localcontext() as ctx:
    ...     ctx.rounding = decimal.ROUND_DOWN
    ...     tax = (price * rate).quantize(PENNY)
    >>> print(f"Tax={tax}")
    Tax=0.11
"""

# With statement example 3 -- logging level change -- perhaps not ideal
# There are better ways to accomplish this.

import logging, sys

class Debugging:

    def __init__(self, aName=None):
        self.logname = aName

    def __enter__(self):
        self.default = logging.getLogger(self.logname).getEffectiveLevel()
        logging.getLogger().setLevel(logging.DEBUG)

    def __exit__(self, exc_type, exc_value, traceback):
        logging.getLogger(self.logname).setLevel(self.default)

test_debugging = """
    >>> import io
    >>> log_file = io.StringIO()
    >>> logging.basicConfig(stream=log_file, level=logging.INFO)
    >>> logging.info("Before")
    >>> logging.debug("Silenced before")
    >>> with Debugging():
    ...     logging.info("During")
    ...     logging.debug("Enabled during")
    >>> logging.info("Between")
    >>> logging.debug("Silenced between")
    >>> with Debugging():
    ...    logging.info("Again")
    ...    logging.debug("Enabled Again")
    >>> logging.info("Done")
    >>> logging.debug("Silenced at the end")
    >>> print(log_file.getvalue())
    INFO:root:Before
    INFO:root:During
    DEBUG:root:Enabled during
    INFO:root:Between
    INFO:root:Again
    DEBUG:root:Enabled Again
    INFO:root:Done
    <BLANKLINE>
"""

# With statement example 4 -- sets the random seed value.

import random
from typing import Optional, Type
from types import TracebackType

class KnownSequence:

    def __init__(self, seed: int = 0) -> None:
        self.seed = 0

    def __enter__(self) -> 'KnownSequence':
        self.was = random.getstate()
        random.seed(self.seed, version=1)
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was)
        return False

test_known_sequence = """
    >>> print(tuple(random.randint(-1, 36) for i in range(5)))  # doctest: +ELLIPSIS
    (...)
    >>> with KnownSequence():
    ...    print(tuple(random.randint(-1, 36) for i in range(5)))
    (23, 25, 1, 15, 31)
    >>> print(tuple(random.randint(-1, 36) for i in range(5)))  # doctest: +ELLIPSIS
    (...)
    >>> with KnownSequence():
    ...    print(tuple(random.randint(-1, 36) for i in range(5)))
    (23, 25, 1, 15, 31)
    >>> print(tuple(random.randint(-1, 36) for i in range(5)))  # doctest: +ELLIPSIS
    (...)
"""

# Some classes for example 5

from typing import NamedTuple
from enum import Enum

class Suit(Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"

class Card(NamedTuple):
    rank: int
    suit: Suit

class Deck(list):

    def __init__(self, size: int = 1) -> None:
        super().__init__()
        for d in range(size):
            cards = [Card(r, s) for r in range(13) for s in cast(Iterable[Suit], Suit)]
            super().extend(cards)
        random.shuffle(self)


# Exam[le 5 -- A Context Manager as Factory example

class Deterministic_Deck:

    def __init__(self, *args, **kw) -> None:
        self.args = args
        self.kw = kw

    def __enter__(self) -> Deck:
        self.was = random.getstate()
        random.seed(0, version=1)
        return Deck(*self.args, **self.kw)

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was)
        return False


test_deterministic_deck = """
    Random
    >>> for i in range(3):
    ...    d1 = Deck()
    ...    print(d1.pop(), d1.pop(), d1.pop())  # doctest: +ELLIPSIS
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)

    Known
    >>> for i in range(3):
    ...     with Deterministic_Deck(1) as dd1:
    ...        print(dd1.pop(), dd1.pop(), dd1.pop())
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)

"""

# Example 6 -- A Context Manager as Mixin

class Deck2(list, KnownSequence):

    def __init__(self, size: int = 1) -> None:
        super().__init__()
        for d in range(size):
            cards = [Card(r, s) for r in range(13) for s in cast(Iterable[Suit], Suit)]
            super().extend(cards)
        self.raw = True
        KnownSequence.__init__(self)

    def pop(self, *args, **kw) -> Card:
        if self.raw:
            random.shuffle(self)
            self.raw = False
        return super().pop(*args, **kw)

test_context_mixin = """
    Random
    >>> for i in range(3):
    ...    dd2r = Deck2()
    ...    print(dd2r.pop(), dd2r.pop(), dd2r.pop())  # doctest: +ELLIPSIS
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)
    Card(rank=..., suit=...) Card(rank=..., suit=...) Card(rank=..., suit=...)
    
    Known 
    >>> for i in range(3):
    ...     with Deck2(1) as dd2k:
    ...        print(dd2k.pop(), dd2k.pop(), dd2k.pop())
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)
    Card(rank=6, suit=<Suit.Clubs: '♣'>) Card(rank=12, suit=<Suit.Clubs: '♣'>) Card(rank=6, suit=<Suit.Hearts: '♥'>)
"""

# Example 7 -- A Context Manager for a File Copy

from pathlib import Path
from typing import Optional

class Updating:

    def __init__(self, target: Path) -> None:
        self.target: Path = target
        self.previous: Optional[Path] = None

    def __enter__(self) -> None:
        try:
            self.previous = (
                self.target.parent
                    / (self.target.stem + " backup")
                ).with_suffix(self.target.suffix)
            self.target.rename(self.previous)
        except FileNotFoundError:
            # Target doesn't exist. That's okay.
            self.previous = None

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        if exc_type is not None:
            # An Exception Occurred: Preserve the erroneous file, if possible.
            try:
                self.failure = (
                    self.target.parent / (self.target.stem + " error")
                    ).with_suffix(self.target.suffix)
                self.target.rename(self.failure)
            except FileNotFoundError:
                pass  # Never even got created.
            # If there was a previous file, put the old file back in place.
            if self.previous:
                self.previous.rename(self.target)
        return False

def some_update(important_path):
    with Updating(important_file):
        with important_file.open('w') as revision:
            revision.write("Attempted Update\\n")
            raise Exception("oops")


test_updating_context = """
    Our file. Make sure it's gone.
    >>> important_file = Path.cwd()/"data"/"some_file.txt"
    >>> try:
    ...     important_file.unlink()
    ... except IOError as e:
    ...     pass
    
    First. Create the data.
    >>> with important_file.open('w') as original:
    ...     _ = original.write("Original data\\n")
    
    Second. Try the update.
    >>> try:
    ...     with Updating(important_file):
    ...         with important_file.open('w') as revision:
    ...             _ = revision.write("Attempted Update\\n")
    ...             raise Exception("oops")
    ... except Exception as ex:
    ...     print(ex)
    oops
    
    # ``some_file error.txt`` left for us to examine.
    # ``some_file.txt`` left intact
    >>> important_file.read_text()
    'Original data\\n'
    
    >>> (Path.cwd()/"data"/"some_file error.txt").read_text()
    'Attempted Update\\n'
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
