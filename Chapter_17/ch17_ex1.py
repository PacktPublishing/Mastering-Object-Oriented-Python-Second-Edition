#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 17. Example 1.
"""

# Card and Deck
# ========================

from typing import Type, cast, Callable
import enum


class Suit(enum.Enum):
    CLUB = "♣"
    DIAMOND = "♦"
    HEART = "♥"
    SPADE = "♠"


class Card:

    def __init__(
        self, rank: int, suit: Suit, hard: int = None, soft: int = None
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard or int(rank)
        self.soft = soft or int(rank)

    def __str__(self) -> str:
        return f"{self.rank!s}{self.suit.value!s}"


class AceCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 1, 11)


class FaceCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)


class LogicError(Exception):
    pass


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard(rank, suit)
    elif 2 <= rank < 11:
        return Card(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit)
    else:
        raise LogicError(f"Rank {rank} invalid")


import random


class Deck1(list):

    def __init__(self, size: int = 1) -> None:
        super().__init__()
        self.rng = random.Random()
        for d in range(size):
            for s in iter(Suit):
                cards: List[Card] = (
                    [cast(Card, AceCard(1, s))]
                    + [Card(r, s) for r in range(2, 12)]
                    + [FaceCard(r, s) for r in range(12, 14)]
                )
                super().extend(cards)
        self.rng.shuffle(self)


class Deck2(list):

    def __init__(
        self,
        size: int = 1,
        random: random.Random = random.Random(),
        ace_class: Type[Card] = AceCard,
        card_class: Type[Card] = Card,
        face_class: Type[Card] = FaceCard,
    ) -> None:
        super().__init__()
        self.rng = random
        for d in range(size):
            for s in iter(Suit):
                cards = (
                    [ace_class(1, s)]
                    + [card_class(r, s) for r in range(2, 12)]
                    + [face_class(r, s) for r in range(12, 14)]
                )
                super().extend(cards)
        self.rng.shuffle(self)


# Card Test
# ========================

# Some Test Cases

import unittest


class TestCard(unittest.TestCase):

    def setUp(self) -> None:
        self.three_clubs = Card(3, Suit.CLUB)

    def test_should_returnStr(self) -> None:
        self.assertEqual("3♣", str(self.three_clubs))

    def test_should_getAttrValues(self) -> None:
        self.assertEqual(3, self.three_clubs.rank)
        self.assertEqual(Suit.CLUB, self.three_clubs.suit)
        self.assertEqual(3, self.three_clubs.hard)
        self.assertEqual(3, self.three_clubs.soft)


class TestAceCard(unittest.TestCase):

    def setUp(self) -> None:
        self.ace_spades = AceCard(1, Suit.SPADE)

    @unittest.expectedFailure
    def test_should_returnStr(self) -> None:
        self.assertEqual("A♠", str(self.ace_spades))

    def test_should_getAttrValues(self) -> None:
        self.assertEqual(1, self.ace_spades.rank)
        self.assertEqual(Suit.SPADE, self.ace_spades.suit)
        self.assertEqual(1, self.ace_spades.hard)
        self.assertEqual(11, self.ace_spades.soft)


class TestFaceCard(unittest.TestCase):

    def setUp(self) -> None:
        self.queen_hearts = FaceCard(12, Suit.HEART)

    @unittest.expectedFailure
    def test_should_returnStr(self) -> None:
        self.assertEqual("Q♥", str(self.queen_hearts))

    def test_should_getAttrValues(self) -> None:
        self.assertEqual(12, self.queen_hearts.rank)
        self.assertEqual(Suit.HEART, self.queen_hearts.suit)
        self.assertEqual(10, self.queen_hearts.hard)
        self.assertEqual(10, self.queen_hearts.soft)


# Suite


def suite2() -> unittest.TestSuite:
    s = unittest.TestSuite()
    load_from = unittest.defaultTestLoader.loadTestsFromTestCase
    s.addTests(load_from(TestCard))
    s.addTests(load_from(TestAceCard))
    s.addTests(load_from(TestFaceCard))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite2())


# Card Factory Test
# =============================

# Another Test Case


class TestCardFactory(unittest.TestCase):

    def test_rank1_should_createAceCard(self) -> None:
        c = card(1, Suit.CLUB)
        self.assertIsInstance(c, AceCard)

    def test_rank2_should_createCard(self) -> None:
        c = card(2, Suit.DIAMOND)
        self.assertIsInstance(c, Card)

    def test_rank10_should_createCard(self) -> None:
        c = card(10, Suit.HEART)
        self.assertIsInstance(c, Card)

    def test_rank10_should_createFaceCard(self) -> None:
        c = card(11, Suit.SPADE)
        self.assertIsInstance(c, Card)

    def test_rank13_should_createFaceCard(self) -> None:
        c = card(13, Suit.CLUB)
        self.assertIsInstance(c, Card)

    def test_otherRank_should_exception(self) -> None:
        with self.assertRaises(LogicError):
            c = card(14, Suit.DIAMOND)
        with self.assertRaises(LogicError):
            c = card(0, Suit.DIAMOND)


# Another Suite


def suite3() -> unittest.TestSuite:
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestCardFactory))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite3())

# Deck with Mock Card
# ==============================

# Class Definitions


class DeckEmpty(Exception):
    pass


class Deck3(list):

    def __init__(
        self,
        size: int = 1,
        random: random.Random = random.Random(),
        card_factory: Callable[[int, Suit], Card] = card,
    ) -> None:
        super().__init__()
        self.rng = random
        for d in range(size):
            super().extend(
                [card_factory(r, s) for r in range(1, 14) for s in iter(Suit)]
            )
        self.rng.shuffle(self)

    def deal(self) -> Card:
        try:
            return self.pop(0)
        except IndexError:
            raise DeckEmpty()


# Test Cases

import unittest
import unittest.mock


class TestDeckBuild(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_card = unittest.mock.Mock(return_value=unittest.mock.sentinel.card)
        self.mock_rng = unittest.mock.Mock(wraps=random.Random())
        self.mock_rng.shuffle = unittest.mock.Mock()

    def test_Deck3_should_build(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)
        self.assertEqual(52 * [unittest.mock.sentinel.card], d)
        self.mock_rng.shuffle.assert_called_with(d)
        self.assertEqual(52, len(self.mock_card.mock_calls))
        expected = [
            unittest.mock.call(r, s)
            for r in range(1, 14)
            for s in (Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE)
        ]
        self.assertEqual(expected, self.mock_card.mock_calls)


class TestDeckDeal(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_deck = [getattr(unittest.mock.sentinel, str(x)) for x in range(52)]
        self.mock_card = unittest.mock.Mock(side_effect=self.mock_deck)
        self.mock_rng = unittest.mock.Mock(wraps=random.Random())
        self.mock_rng.shuffle = unittest.mock.Mock()

    def test_Deck3_should_deal(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)
        dealt = []
        for i in range(52):
            card = d.deal()
            dealt.append(card)
        self.assertEqual(dealt, self.mock_deck)

    def test_empty_deck_should_exception(self) -> None:
        d = Deck3(size=1, random=self.mock_rng, card_factory=self.mock_card)
        for i in range(52):
            card = d.deal()
        self.assertRaises(DeckEmpty, d.deal)


# Suite


def suite4():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDeckBuild))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDeckDeal))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite4())

# Doctest
# ===============

# Sample Function with doctest string


def ackermann(m: int, n: int) -> int:
    """Ackermann's Function
    ackermann(m, n) = $2 \\uparrow^{m-2} (n+3)-3$

    See http://en.wikipedia.org/wiki/Ackermann_function and
    http://en.wikipedia.org/wiki/Knuth%27s_up-arrow_notation.

    >>> from Chapter_17.ch17_ex1 import ackermann
    >>> ackermann(2,4)
    11
    >>> ackermann(0,4)
    5
    >>> ackermann(1,0)
    2
    >>> ackermann(1,1)
    3

    """
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    else:
        raise LogicError()


if __name__ == "__main__":
    import doctest

    suite5 = doctest.DocTestSuite()
    t = unittest.TextTestRunner(verbosity=2)
    t.run(suite5)


# Combined Testing
# =========================

# Main Program to combine suites

if __name__ == "__main__":
    all_tests = unittest.TestSuite()
    all_tests.addTests(suite2())
    all_tests.addTests(suite3())
    all_tests.addTests(suite4())
    all_tests.addTests(suite5)
    t = unittest.TextTestRunner()
    t.run(all_tests)

# OS testing
# ======================

# Functions to test

from collections import defaultdict
from typing import NamedTuple, Dict, List


class GameStat(NamedTuple):
    player: str
    bet: str
    rounds: int
    final: int


import csv
from pathlib import Path
from typing import Iterable, Iterator, Dict, DefaultDict, List


def gamestat_iter(source: Iterable[Dict[str, str]]) -> Iterator[GameStat]:
    for row in source:
        yield GameStat(row["player"], row["bet"], int(row["rounds"]), int(row["final"]))


def rounds_final(path: Path) -> DefaultDict[int, List[int]]:
    stats: DefaultDict[int, List[int]] = defaultdict(list)
    with path.open() as source:
        reader = csv.DictReader(source)
        assert set(reader.fieldnames) == set(GameStat._fields)
        for gs in gamestat_iter(reader):
            stats[gs.rounds].append(gs.final)
    return stats


# Two approaches:
#
# - io.StringIO()
#
# - create a file

# We might want to test missing or damaged file features, in which
# case StringIO doesn't work as well as creating a file.

# Test Cases

import os


class Test_Missing(unittest.TestCase):

    def setUp(self) -> None:
        try:
            (Path.cwd() / "data" / "ch17_sample.csv").unlink()
            # print(f"setUp removed {(Path.cwd()/"data"/"ch17_sample.csv")}")
        except OSError as e:
            pass
            # print("setUp expected", e)

    def test_missingFile_should_returnDefault(self) -> None:
        self.assertRaises(
            FileNotFoundError, rounds_final, (Path.cwd() / "data" / "ch17_sample.csv")
        )


class Test_Damaged(unittest.TestCase):

    def setUp(self) -> None:
        with (Path.cwd() / "data" / "ch17_sample.csv").open("w") as target:
            print("not_player,bet,rounds,final", file=target)
            print("data,1,1,1", file=target)

    def test_damagedFile_should_raiseException(self) -> None:
        self.assertRaises(
            AssertionError, rounds_final, (Path.cwd() / "data" / "ch17_sample.csv")
        )


def suite7():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Missing))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Damaged))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite7())

# External CSV Examples
# ======================

# Unit Under Test

from Chapter_4.ch04_ex3 import RateTimeDistance, RTD_Dynamic

# Sample data

sample_data = """\
rate_in,time_in,distance_in,rate_out,time_out,distance_out
2,3,,2,3,6
5,,7,5,1.4,7
,11,13,1.18,11,13
"""

# Parse the sample data

from typing import Optional
import csv


def float_or_none(text: str) -> Optional[float]:
    if len(text) == 0:
        return None
    return float(text)


# TestCase with only one test method


class Test_RTD(unittest.TestCase):

    def runTest(self) -> None:
        with (Path.cwd() / "data" / "ch17_data.csv").open() as source:
            rdr = csv.DictReader(source)
            for row in rdr:
                self.example(**row)

    def example(
        self,
        rate_in: str,
        time_in: str,
        distance_in: str,
        rate_out: str,
        time_out: str,
        distance_out: str,
    ) -> None:
        args = dict(
            rate=float_or_none(rate_in),
            time=float_or_none(time_in),
            distance=float_or_none(distance_in),
        )
        expected = dict(
            rate=float(rate_out), time=float(time_out), distance=float(distance_out)
        )
        rtd = RateTimeDistance(**args)
        assert rtd.distance and rtd.rate and rtd.time
        self.assertAlmostEqual(rtd.distance, rtd.rate * rtd.time, places=2)
        self.assertAlmostEqual(rtd.rate, expected["rate"], places=2)
        self.assertAlmostEqual(rtd.time, expected["time"], places=2)
        self.assertAlmostEqual(rtd.distance, expected["distance"], places=2)


# Build Suite from user-supplied sample data

with (Path.cwd() / "data" / "ch17_data.csv").open("w", newline="") as target:
    target.write(sample_data)


def suite9():
    suite = unittest.TestSuite()
    suite.addTest(Test_RTD())
    return suite


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite9())

# Performance Testing
# ======================

# Using unittest for this is a bit "forced." We don't really need unittest framework
# for this.

import unittest
import timeit


class Test_Performance(unittest.TestCase):

    def test_simpleCalc_shouldbe_fastEnough(self):
        t = timeit.timeit(
            stmt="""RateTimeDistance(rate=1, time=2)""",
            setup="""from Chapter_4.ch04_ex3 import RateTimeDistance""",
        )
        print("Run time", t)
        self.assertLess(t, 10, f"run time {t} >= 10")


# Make a suite of the testcases


def suite10():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Performance))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite10())
