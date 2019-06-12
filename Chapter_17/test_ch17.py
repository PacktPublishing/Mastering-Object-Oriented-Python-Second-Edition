#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 17. Example 2.

..  note::

    This example's name, ``test_ch17.py`` is chosen to help pytest
    do test discovery.
"""

# Card and Deck
# ========================

import enum
from typing import cast, Type
import random

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
from pytest import mark


def test_card():
    three_clubs = Card(3, Suit.CLUB)
    assert "3♣" == str(three_clubs)
    assert 3 == three_clubs.rank
    assert Suit.CLUB == three_clubs.suit
    assert 3 == three_clubs.hard
    assert 3 == three_clubs.soft

@mark.xfail
def test_ace_card():
    ace_spades = AceCard(1, Suit.SPADE)
    assert "A♠" == str(ace_spades), "This is expected to fail"
    assert 1 == ace_spades.rank
    assert Suit.SPADE == ace_spades.suit
    assert 1 == ace_spades.hard
    assert 11 == ace_spades.soft

@mark.xfail
def test_face_card():
    queen_hearts = FaceCard(12, Suit.HEART), "This is expected to fail"
    assert "Q♥" == str(queen_hearts)
    assert 12 == queen_hearts.rank
    assert Suit.HEART == queen_hearts.suit
    assert 10 == queen_hearts.hard
    assert 10 == queen_hearts.soft


# Suites -- not relevant for pytest -- the test discovery handles this.


# Card Factory Test
# =============================

# Another Test Case

from pytest import raises

def test_card_factory():

    c1 = card(1, Suit.CLUB)
    assert isinstance(c1, AceCard)

    c2 = card(2, Suit.DIAMOND)
    assert isinstance(c1, Card)

    c10 = card(10, Suit.HEART)
    assert isinstance(c10, Card)

    cj = card(11, Suit.SPADE)
    assert isinstance(cj, FaceCard)

    ck = card(13, Suit.CLUB)
    assert isinstance(ck, FaceCard)

    with raises(LogicError):
        c14 = card(14, Suit.DIAMOND)

    with raises(LogicError):
        c0 = card(0, Suit.DIAMOND)


# Deck with Mock Card
# ==============================

# Class Definitios


class DeckEmpty(Exception):
    pass


class Deck3(list):

    def __init__(self, size=1, random=random.Random(), card_factory=card):
        super().__init__()
        self.rng = random
        for d in range(size):
            super().extend([card_factory(r, s) for r in range(1, 14) for s in iter(Suit)])
        self.rng.shuffle(self)

    def deal(self):
        try:
            return self.pop(0)
        except IndexError:
            raise DeckEmpty()


# Test Cases

import unittest.mock
from types import SimpleNamespace
from pytest import fixture

@fixture
def deck_context():
    mock_deck = [
        getattr(unittest.mock.sentinel, str(x))
        for x in range(52)
    ]
    mock_card = unittest.mock.Mock(side_effect=mock_deck)
    mock_rng = unittest.mock.Mock(
        wraps=random.Random,
        shuffle=unittest.mock.Mock(return_value=None)
    )
    return SimpleNamespace(**locals())


def test_deck_build(deck_context):
    d = Deck3(
        size=1,
        random=deck_context.mock_rng,
        card_factory=deck_context.mock_card
    )
    deck_context.mock_rng.shuffle.assert_called_once_with(d)
    assert 52 == len(deck_context.mock_card.mock_calls)
    expected = [
        unittest.mock.call(r, s) for r in range(1, 14) for s in iter(Suit)
    ]
    assert expected == deck_context.mock_card.mock_calls


def test_deck_deal(deck_context):
    d = Deck3(
        size=1,
        random=deck_context.mock_rng,
        card_factory=deck_context.mock_card
    )
    dealt = []
    for c in range(52):
        c = d.deal()
        dealt.append(c)
    assert deck_context.mock_deck == dealt

    with raises(DeckEmpty):
        extra = d.deal()

# Doctest
# ===============

# Sample Function with doctest string. pytest finds these, too.


def ackermann(m, n):
    """Ackermann's Function
    ackermann(m, n) = $2 \\uparrow^{m-2} (n+3)-3$

    See http://en.wikipedia.org/wiki/Ackermann_function and
    http://en.wikipedia.org/wiki/Knuth%27s_up-arrow_notation.

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


def gamestat_iter(iterator):
    for row in iterator:
        yield GameStat(row["player"], row["bet"], int(row["rounds"]), int(row["final"]))


def rounds_final(path: Path):
    stats: Dict[int, List[int]] = defaultdict(list)
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

from pytest import fixture, mark

@fixture
def no_file_path():
    file_path = Path.cwd() / "data" / "ch17_sample.csv"
    try:
        file_path.unlink()
        # print(f"no_file_path fixture removed {file_path}")
    except FileNotFoundError as e:
        pass
    yield file_path
    # Cleanup can go here

def test_missing(no_file_path):
    with raises(FileNotFoundError):
        rounds_final(no_file_path)


@fixture
def damaged_file_path():
    file_path = Path.cwd() / "data" / "ch17_sample.csv"
    with file_path.open("w", newline="") as target:
        print("not_player,bet,rounds,final", file=target)
        print("data,1,1,1", file=target)
    yield file_path
    file_path.unlink()

def test_damaged(damaged_file_path):
    with raises(AssertionError):
        stats = rounds_final(Path.cwd()/"data"/"ch17_sample.csv")


# SQLite testing
# =========================

# This is integration testing, not unit testing.
# Integration means we use the database
# instead of isolating our code from the database.
# A more formal unit test would mock the database layer.

# SQLAlchemy ORM classes

from Chapter_12.ch12_ex4 import Base, Blog, Post, Tag, assoc_post_tag
import datetime

# Create Test Database and Schema

import sqlalchemy.exc
from sqlalchemy import create_engine


def built_test_db(name="sqlite:///./data/ch17_blog.db"):
    engine = create_engine(name, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine

# Unittest Case

from sqlalchemy.orm import sessionmaker

@fixture(scope="module")
def db_session_maker():
    engine = built_test_db()
    session_maker = sessionmaker(bind=engine)

    session = session_maker()
    tag_rr = Tag(phrase="#RedRanger")
    session.add(tag_rr)
    tag_w42 = Tag(phrase="#Whitby42")
    session.add(tag_w42)
    tag_icw = Tag(phrase="#ICW")
    session.add(tag_icw)
    tag_mis = Tag(phrase="#Mistakes")
    session.add(tag_mis)

    blog1 = Blog(title="Travel 2013")
    session.add(blog1)
    b1p1 = Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓︎""",
        blog=blog1,
        tags=[tag_rr, tag_w42, tag_icw],
    )
    session.add(b1p1)
    b1p2 = Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including ☺ and ☀︎︎""",
        blog=blog1,
        tags=[tag_rr, tag_w42, tag_mis],
    )
    session.add(b1p2)

    blog2 = Blog(title="Travel 2014")
    session.add(blog2)
    session.commit()
    return session_maker

def test_database(db_session_maker):

    db_session = db_session_maker()

    # Tests schema definition
    results = db_session.query(Blog).filter(Blog.title == "Travel 2013").all()
    assert 1 == len(results)
    assert 2 == len(results[0].entries)

    # Tests SQLAlchemy, and test data
    results = db_session.query(Blog).filter(Blog.title.like("Travel %")).all()
    assert 2 == len(results)

    results = db_session.query(Post).join(assoc_post_tag).join(Tag).filter(
        Tag.phrase == "#Whitby42"
    ).all()
    assert 2 == len(results)

    results = db_session.query(Post).join(assoc_post_tag).join(Tag).filter(
        Tag.phrase == "#ICW"
    ).all()
    # print( [r.title for r in results] )
    assert 1 == len(results)
    assert "Hard Aground" == results[0].title
    assert "Travel 2013" == results[0].blog.title
    assert set(["#RedRanger", "#Whitby42", "#ICW"]) == set(t.phrase for t in results[0].tags)

# External CSV Examples
# ======================

# Unit Under Test

from Chapter_4.ch04_ex3 import RateTimeDistance
from pytest import approx

# Parsing the sample data

def float_or_none(text):
    if len(text) == 0:
        return None
    return float(text)

# Build Suite from user-supplied sample data

import csv

with (Path.cwd() / "Chapter_17" / "ch17_data.csv").open() as source:
    rdr = csv.DictReader(source)
    rtd_cases = list(rdr)

@fixture(params=rtd_cases)
def rtd_example(request):
    """Each request will include a param. This will be a row from the source cases."""
    yield request.param

def test_rtd(rtd_example):
    args = dict(
        rate=float_or_none(rtd_example['rate_in']),
        time=float_or_none(rtd_example['time_in']),
        distance=float_or_none(rtd_example['distance_in']),
    )
    result = dict(
        rate=float_or_none(rtd_example['rate_out']),
        time=float_or_none(rtd_example['time_out']),
        distance=float_or_none(rtd_example['distance_out']),
    )
    # print(f"***{args}***")

    rtd = RateTimeDistance(**args)

    assert rtd.distance == approx(rtd.rate * rtd.time)
    assert rtd.rate == approx(result["rate"], abs=1E-2)
    assert rtd.time == approx(result["time"])
    assert rtd.distance == approx(result["distance"])




# Performance Testing
# ======================

# This can be used stand-alone, or with pytest.

import timeit

def test_performance():

    t = timeit.timeit(
        stmt="""RateTimeDistance( rate=1, time=2 )""",
        setup="""from Chapter_4.ch04_ex3 import RateTimeDistance""",
    )
    print("Run time", t)
    assert t < 10, f"run time {t} >= 10"
