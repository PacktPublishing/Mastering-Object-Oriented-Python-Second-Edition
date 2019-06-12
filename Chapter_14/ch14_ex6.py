#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 14. Example 6.
"""

from Chapter_14.simulation_model import *

# A typical main program using the above class definitions

from pathlib import Path
from typing import List, Any, TextIO, Iterator, Union
import csv
from collections import ChainMap
import ast

# Exec Import
# ################

import io

# JSON or YAML files
# ===================

# JSON using dictionary-of-dictionaries nested structures.
# This is inconvenient to handle multiple configuration files.
import io


# XML files
# ==========

# Plist
# #######

# Sample PLIST Document. As bytes.
import io

plist_file = io.BytesIO(
    b"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>player</key>
    <dict>
        <key>betting</key>
        <string>Flat</string>
        <key>play</key>
        <string>SomeStrategy</string>
        <key>rounds</key>
        <integer>100</integer>
        <key>stake</key>
        <integer>50</integer>
    </dict>
    <key>simulator</key>
    <dict>
        <key>outputfile</key>
        <string>ch14_simulation6a.dat</string>
        <key>samples</key>
        <integer>100</integer>
    </dict>
    <key>table</key>
    <dict>
        <key>dealer</key>
        <string>Hit17</string>
        <key>decks</key>
        <integer>6</integer>
        <key>limit</key>
        <integer>50</integer>
        <key>payout</key>
        <array>
            <integer>3</integer>
            <integer>2</integer>
        </array>
        <key>split</key>
        <string>NoResplitAces</string>
    </dict>
</dict>
</plist>
"""
)

import plistlib
print(plistlib.load(plist_file))

# Non-Plist
# ##########

# A completely customized XML document
import io

xml_file = io.BytesIO(
    b"""<?xml version="1.0" encoding="UTF-8"?>
<simulation>
    <table>
        <dealer>Hit17</dealer>
        <split>NoResplitAces</split>
        <decks>6</decks>
        <limit>50</limit>
        <payout>(3,2)</payout>
    </table>
    <player>
        <betting>Flat</betting>
        <play>SomeStrategy</play>
        <rounds>100</rounds>
        <stake>50</stake>
    </player>
    <simulator>
        <outputfile>data/ch14_simulation6b.dat</outputfile>
        <samples>100</samples>
    </simulator>
</simulation>
"""
)

import xml.etree.ElementTree as XML


class Configuration:

    def read_file(self, file):
        self.config = XML.parse(file)

    def read(self, filename):
        self.config = XML.parse(filename)

    def read_string(self, text):
        self.config = XML.fromstring(text)

    def get(self, qual_name, default):
        section, _, item = qual_name.partition(".")
        query = "./{0}/{1}".format(section, item)
        node = self.config.find(query)
        if node is None:
            return default
        return node.text

    def __getitem__(self, section):
        query = "./{0}".format(section)
        parent = self.config.find(query)
        return dict((item.tag, item.text) for item in parent)

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
    player = Player(play=player_rule, betting=betting_rule, max_rounds=rounds, init_stake=stake)

    outputfile = config.get("simulator.outputfile", "blackjack.csv")
    samples = int(config.get("simulator.samples", 100))
    simulator = Simulate(table, player, samples)
    with open(outputfile, "w", newline="") as results:
        wtr = csv.writer(results)
        for gamestats in simulator:
            wtr.writerow(gamestats)


if __name__ == "__main__":

    config = Configuration()
    config.read_file(xml_file)
    main_cm_prop(config)
    check(Path(config["simulator"]["outputfile"]))


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
