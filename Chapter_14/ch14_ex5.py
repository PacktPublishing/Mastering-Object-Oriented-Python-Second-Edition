#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 5.
"""

from Chapter_14.simulation_model import *

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union, IO, cast
import csv
from collections import ChainMap

import io

# Property files
# ===============

# - Lines have keys and values.
# - Key ends with the first unescaped '=', ':', or white space character.
# - Value is optional and defaults to "".
# - Number sign (#) or the exclamation mark (!) as
#   the first non blank character in a line is a comment.
# - The backwards slash is used to escape a character.
# - Since  #, !, =, and : have meaning,
#   when involved in a piece of key or element, use a preceding backslash
# - Key with spaces is tolerated using '\ '.
# - Key or value with newline is tolerated using '\\n'.
# - Unicode escapes may be used:  \uxxxx is the format.
# - Everything is text, explicit conversions required

# Example 1
# From http://en.wikipedia.org/wiki/.properties
prop1 = """
# You are reading the ".properties" entry.
! The exclamation mark can also mark text as comments.
# The key and element characters #, !, =, and : are written with a preceding backslash to ensure that they are properly loaded.
website = http\://en.wikipedia.org/
language = English
# The backslash below tells the application to continue reading
# the value onto the next line.
message = Welcome to \\
          Wikipedia\!
# Add spaces to the key
key\ with\ spaces = This is the value that could be looked up with the key "key with spaces".
# Unicode
tab : \\u0009
"""

# Example 2
# From http://docs.oracle.com/javase/7/docs/api/java/util/Properties.html
prop2 = """
\:\=
Truth = Beauty
 Truth:Beauty
Truth                    :Beauty

fruits                          apple, banana, pear, \\
                                cantaloupe, watermelon, \\
                                kiwi, mango

cheeses
"""

# Property File Parsing Class
import re


class PropertyParser:

    def read_string(self, data: str) -> Iterator[Tuple[str, str]]:
        return self._parse(data)

    def read_file(self, file: IO[str]) -> Iterator[Tuple[str, str]]:
        data = file.read()
        return self.read_string(data)

    def read(self, path: Path) -> Iterator[Tuple[str, str]]:
        with path.open("r") as file:
            return self.read_file(file)

    key_element_pat = re.compile(r"(.*?)\s*(?<!\\)[:=\s]\s*(.*)")

    def _parse(self, data: str) -> Iterator[Tuple[str, str]]:
        logical_lines = (
            line.strip() for line in re.sub(r"\\\n\s*", "", data).splitlines()
        )
        non_empty = (line for line in logical_lines if len(line) != 0)
        non_comment = (
            line
            for line in non_empty
            if not (line.startswith("#") or line.startswith("!"))
        )
        for line in non_comment:
            ke_match = self.key_element_pat.match(line)
            if ke_match:
                key, element = ke_match.group(1), ke_match.group(2)
            else:
                key, element = line, ""
            key = self._escape(key)
            element = self._escape(element)
            yield key, element

    def load(
        self, file_name_or_path: Union[TextIO, str, Path]
    ) -> Iterator[Tuple[str, str]]:
        if isinstance(file_name_or_path, io.TextIOBase):
            return self.loads(file_name_or_path.read())
        else:
            name_or_path = cast(Union[str, Path], file_name_or_path)
            with Path(name_or_path).open("r") as file:
                return self.loads(file.read())

    def loads(self, data: str) -> Iterator[Tuple[str, str]]:
        return self._parse(data)

    def _escape(self, data: str) -> str:
        d1 = re.sub(r"\\([:#!=\s])", lambda x: x.group(1), data)
        d2 = re.sub(r"\\u([0-9A-Fa-f]+)", lambda x: chr(int(x.group(1), 16)), d1)
        return d2

    def _escape2(self, data: str) -> str:
        d2 = re.sub(
            r"\\([:#!=\s])|\\u([0-9A-Fa-f]+)",
            lambda x: x.group(1) if x.group(1) else chr(int(x.group(2), 16)),
            data,
        )
        return d2


test_should_parse_prop1 = """
A test for the prop1 example. We can create a dict since each key is unique.

>>> parser = PropertyParser()
>>> actual = dict(parser.read_string(prop1))
>>> expected = {
...    "key with spaces": 'This is the value that could be looked up with the key "key with spaces".',
...    "language": "English",
...    "message": "Welcome to Wikipedia!",
...    "tab": "\\t",
...    "website": "http://en.wikipedia.org/",
... }
>>> expected == actual
True
"""

test_should_parse_prop2 = """
A test for the prop2 example. We create a list since each key is not unique.

>>> parser = PropertyParser()
>>> actual = list(parser.read_string(prop2))
>>> expected = [
...    (":=", ""),
...    ("Truth", "Beauty"),
...    ("Truth", "Beauty"),
...    ("Truth", "Beauty"),
...    ("fruits", "apple, banana, pear, cantaloupe, watermelon, kiwi, mango"),
...    ("cheeses", ""),
... ]
>>> expected == actual
True
>>> actual
[(':=', ''), ('Truth', 'Beauty'), ('Truth', 'Beauty'), ('Truth', 'Beauty'), ('fruits', 'apple, banana, pear, cantaloupe, watermelon, kiwi, mango'), ('cheeses', '')]
"""

test_edge_case = """
>>> parser = PropertyParser()
>>> prop = "a\:b: value"
>>> actual = list(parser.read_string(prop))
>>> expected = [("a:b", "value")]
>>> actual == expected
True
>>> actual
[('a:b', 'value')]
"""

# Main Program to use property file input
import ast


def main_cm_prop(config):
    dealer_nm = config.get("table.dealer", "Hit17")
    dealer_rule = {"Hit17": Hit17(), "Stand17": Stand17()}.get(dealer_nm, Hit17())
    split_nm = config.get("table.split", "ReSplit")
    split_rule = {
        "ReSplit": ReSplit(), "NoReSplit": NoReSplit(), "NoReSplitAces": NoReSplitAces()
    }.get(
        split_nm, ReSplit()
    )
    decks = int(config.get("table.decks", 6))
    limit = int(config.get("table.limit", 100))
    payout = ast.literal_eval(config.get("table.payout", "(3,2)"))
    table = Table(
        decks=decks, limit=limit, dealer=dealer_rule, split=split_rule, payout=payout
    )

    player_nm = config.get("player.play", "SomeStrategy")
    player_rule = {
        "SomeStrategy": SomeStrategy(), "AnotherStrategy": AnotherStrategy()
    }.get(
        player_nm, SomeStrategy()
    )
    bet_nm = config.get("player.betting", "Flat")
    betting_rule = {
        "Flat": Flat(), "Martingale": Martingale(), "OneThreeTwoSix": OneThreeTwoSix()
    }.get(
        bet_nm, Flat()
    )
    rounds = int(config.get("player.rounds", 100))
    stake = int(config.get("player.stake", 50))
    player = Player(
        play=player_rule, betting=betting_rule, max_rounds=rounds, init_stake=stake
    )

    outputfile = config.get("simulator.outputfile", "blackjack.csv")
    samples = int(config.get("simulator.samples", 100))
    simulator = Simulate(table, player, samples)
    with open(outputfile, "w", newline="") as results:
        wtr = csv.writer(results)
        for gamestats in simulator:
            wtr.writerow(gamestats)


# Example property file.
prop_file = io.StringIO(
"""
# Example Simulation Setup

player.betting: Flat
player.play: SomeStrategy
player.rounds: 100
player.stake: 50

table.dealer: Hit17
table.decks: 6
table.limit: 50
table.payout: (3,2)
table.split: NoResplitAces

simulator.outputfile = data/ch14_simulation5.dat
simulator.samples = 100
"""
)


if __name__ == "__main__":
    from pprint import pprint

    pp = PropertyParser()

    candidate_list = [prop_file]
    properties = [dict(pp.read_file(file)) for file in reversed(candidate_list)]
    pprint(properties)
    config = ChainMap(*properties)

    main_cm_prop(config)
    check(Path(config["simulator.outputfile"]))


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
