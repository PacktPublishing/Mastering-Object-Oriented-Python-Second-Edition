#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 4. CSV
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from typing import List, Optional, Dict, Any, Iterator
from dataclasses import dataclass
from pathlib import Path

from Chapter_10.ch10_ex1 import Post, Blog, travel, rst_render
from Chapter_10.ch10_ex2 import FaceCard, AceCard, Card
import io

# CSV
# ===================

# Example 1: GameStats
# ######################


class Table:
    """Abstraction for games played on tables."""

    def bet(self, game_state: str, amount: float) -> None:
        """Accepts a bet for a particular future game state."""
        pass


class Player_Strategy:
    """Abstraction for player choices. Varies by game, of course."""
    pass


class Betting:

    def __init__(self, stake: float = 100) -> None:
        self.stake = stake

    def bet(self, table: Table, game_state: str) -> None:
        if game_state == "ante":
            table.bet(game_state, 1)

    def win(self, amount: float) -> None:
        self.stake += amount

    def loss(self, amount: float) -> None:
        self.stake -= amount

    def push(self) -> None:
        pass


class Flat_Bet(Betting):
    pass


class Martingale_Bet(Betting):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.stage = 1

    def bet(self, table: Table, game_state: str) -> None:
        if game_state == "ante":
            try:
                table.bet(game_state, min(self.stage, self.stake))
            except BadBet as e:
                limit = e.args[0]
                table.bet(game_state, min(limit, self.stake))

    def win(self, amount) -> None:
        self.stage = 1
        super().win(amount)

    def loss(self, amount) -> None:
        self.stage = min(self.stage * 2, 512)
        super().loss(amount)

    def push(self) -> None:
        super().push()


import random


class BadBet(Exception):
    pass


class Broke(Exception):
    pass


# A "Table" implementation for Blackjack.
class Blackjack(Table):

    def __init__(self, play: Player_Strategy, betting: Betting) -> None:
        self.player = play
        self.betting = betting
        self.bets: Dict[str, float] = dict()
        self.rounds = 0

    @property
    def stake(self) -> float:
        return self.betting.stake

    def bet(self, game_state: str, amount: float) -> None:
        if amount > 50:
            raise BadBet(50)
        self.bets[game_state] = amount

    def play_1(self) -> None:
        if self.betting.stake == 0:
            raise Broke
        self.betting.bet(self, "ante")
        bet = sum(self.bets.values())
        outcome = random.random()
        if outcome < 0.579:
            self.betting.loss(bet)
        elif 0.579 <= outcome < 0.883:
            self.betting.win(bet)
        elif 0.883 <= outcome < 0.943:
            self.betting.push()
        else:
            # 0.943 <= outcome
            self.betting.win(bet * 2)

    def until_broke_or_rounds(self, limit: int) -> None:
        while self.rounds < limit and self.betting.stake > 0:
            self.play_1()
            self.rounds += 1


# Example 1 dumping
# ####################

# An application of the above definitions.
from typing import NamedTuple


class GameStat(NamedTuple):
    player: str
    bet: str
    rounds: int
    final: float


from typing import Iterator, Type


def gamestat_iter(
    player: Type[Player_Strategy], betting: Type[Betting], limit: int = 100
) -> Iterator[GameStat]:
    for sample in range(30):
        random.seed(sample)  # Reproducible
        b = Blackjack(player(), betting())
        b.until_broke_or_rounds(limit)
        yield GameStat(player.__name__, betting.__name__, b.rounds, b.betting.stake)


import csv
from pathlib import Path

with (Path.cwd() / "data" / "ch10_blackjack_1.csv").open("w", newline="") as target:
    writer = csv.DictWriter(target, GameStat._fields)
    writer.writeheader()
    for gamestat in gamestat_iter(Player_Strategy, Martingale_Bet):
        writer.writerow(gamestat._asdict())

data = gamestat_iter(Player_Strategy, Martingale_Bet)
with (Path.cwd() / "data" / "ch10_blackjack_2.csv").open("w", newline="") as target:
    writer = csv.DictWriter(target, GameStat._fields)
    writer.writeheader()
    writer.writerows(g._asdict() for g in data)

# Example 2 loading
# ###################

# Loading data from the simulator

with (Path.cwd() / "data" / "ch10_blackjack_1.csv").open() as source:
    reader = csv.DictReader(source)
    assert set(reader.fieldnames) == set(GameStat._fields)
    for gs in (GameStat(**r) for r in reader):
        pass  # print( gs )


def gamestat_rdr_iter(
        source_data: Iterator[Dict[str, str]]
    ) -> Iterator[GameStat]:
    for row in source_data:
        yield GameStat(row["player"], row["bet"], int(row["rounds"]), int(row["final"]))


test_write_read_1 = """
    >>> with (Path.cwd()/"data"/"ch10_blackjack_1.csv").open() as source:
    ...     reader = csv.DictReader(source)
    ...     assert set(reader.fieldnames) == set(GameStat._fields)
    ...     for gs in gamestat_rdr_iter(reader):
    ...         print(gs)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=142)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=27, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=25, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=157)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=87)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=18, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=161)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=10, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=22, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=53, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=37, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=27, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=188)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=58, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=103)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=28, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=60, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=150)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=9, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=13, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=97, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=100, final=93)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=72, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=12, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=36, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=35, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=78, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=68, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=39, final=0)
    GameStat(player='Player_Strategy', bet='Martingale_Bet', rounds=47, final=0)
"""

# Example 3 blog and post one file
# ################################

# There are two row types, however -- blogs and posts within a blog.

# Our blog data to be saved positionally.
blogs = [travel]

with (Path.cwd() / "data" / "ch10_blog3.csv").open("w", newline="") as target:
    wtr = csv.writer(target)
    wtr.writerow(["__class__", "title", "date", "title", "rst_text", "tags"])
    for b in blogs:
        wtr.writerow(["Blog", b.title, None, None, None, None])
        for p in b.entries:
            wtr.writerow(["Post", None, p.date, p.title, p.rst_text, p.tags])

# Super-important: column order must match __init__() param order.
# Hard to do in general.
# And impossible to make work with mypy unless your Blog and Post structures
# are reduced to List[str]
with (Path.cwd() / "data" / "ch10_blog3.csv").open() as source:
    rdr = csv.reader(source)
    header = next(rdr)
    assert header == ["__class__", "title", "date", "title", "rst_text", "tags"]
    blogs = []
    for r in rdr:
        if r[0] == "Blog":
            blog = Blog(*r[1:2])  # type: ignore
            blogs.append(blog)
        elif r[0] == "Post":
            post = Post(*r[2:])  # type: ignore
            blogs[-1].append(post)

# Tags, however, will not be a proper tuple
# The above doesn't handle Post tags properly!

# Can use the following for safe eval of literals.
import ast


def blog_builder(row: List[str]) -> Blog:
    return Blog(row[1])


def post_builder(row: List[str]) -> Post:
    return Post(
        date=datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
        title=row[3],
        rst_text=row[4],
        tags=ast.literal_eval(row[5]),
    )


with (Path.cwd() / "data" / "ch10_blog3.csv").open() as source:
    rdr = csv.reader(source)
    header = next(rdr)
    assert header == ["__class__", "title", "date", "title", "rst_text", "tags"]
    blogs = []
    for r in rdr:
        if r[0] == "Blog":
            blog = blog_builder(r)
            blogs.append(blog)
        elif r[0] == "Post":
            post = post_builder(r)
            blogs[-1].append(post)

# Example 4 blog and post with better metadata and filter
# ########################################################

# Loading the blog with a generator function.

from typing import TextIO, cast


def blog_iter(source: TextIO) -> Iterator[Blog]:
    rdr = csv.reader(source)
    header = next(rdr)
    assert header == ["__class__", "title", "date", "title", "rst_text", "tags"]
    blog: Blog = cast(Blog, None)
    for r in rdr:
        if r[0] == "Blog":
            if blog:
                yield blog
            blog = blog_builder(r)
        elif r[0] == "Post":
            post = post_builder(r)
            blog.append(post)
    if blog:
        yield blog


test_blog_3 = """
    >>> with (Path.cwd()/"data"/"ch10_blog3.csv").open() as source:
    ...     for b in blog_iter(source):
    ...         print(b.title, [p.title for p in b.entries])
    Travel ['Hard Aground', 'Anchor Follies']

    >>> with (Path.cwd()/"data"/"ch10_blog3.csv").open() as source:
    ...     blogs = list(blog_iter(source))
    >>> for b in blogs:
    ...     print(b.title, [p.title for p in b.entries])
    Travel ['Hard Aground', 'Anchor Follies']
"""

# Example 5 Blog and Post join
# ################################

# Using a "join" between Blog and Post to create a file.
with (Path.cwd() / "data" / "ch10_blog5.csv").open("w", newline="") as target:
    wtr = csv.writer(target)
    wtr.writerow(
        ["Blog.title", "Post.date", "Post.title", "Post.tags", "Post.rst_text"]
    )
    for b in blogs:
        for p in b.entries:
            wtr.writerow([b.title, p.date, p.title, p.tags, p.rst_text])

from typing import Union, Iterator, Tuple


import ast


def post_builder5(row: Dict[str, str]) -> Post:
    return Post(
        date=datetime.datetime.strptime(row["Post.date"], "%Y-%m-%d %H:%M:%S"),
        title=row["Post.title"],
        rst_text=row["Post.rst_text"],
        tags=ast.literal_eval(row["Post.tags"]),
    )


def blog_builder5(row: Dict[str, str]) -> Blog:
    return Blog(title=row["Blog.title"])


from typing import TextIO


def blog_iter2(source: TextIO) -> Iterator[Blog]:
    """An iterator which fetches blogs"""

    rdr = csv.DictReader(source)
    assert (
        set(rdr.fieldnames)
        == {"Blog.title", "Post.date", "Post.title", "Post.tags", "Post.rst_text"}
    )
    # Fetch the first row and build the first Blog and Post from this
    row = next(rdr)
    blog = blog_builder5(row)
    post = post_builder5(row)
    blog.append(post)

    # Fetch all subsequent rows.
    # Emit completed Blogs.
    # Append Posts to the currently open Blog
    for row in rdr:
        if row["Blog.title"] != blog.title:
            yield blog
            blog = blog_builder5(row)
        post = post_builder5(row)
        blog.append(post)
    yield blog


test_blog_iter_2 = """
    >>> with (Path.cwd()/"data"/"ch10_blog5.csv").open() as source:
    ...    for b in blog_iter2(source):
    ...        print(b.title, b.as_dict())
    Travel {'title': 'Travel', 'underline': '======', 'entries': [{'date': '2013-11-14 17:25:00', 'title': 'Hard Aground', 'underline': '------------', 'rst_text': 'Some embarrassing revelation. Including ☹ and ⚓︎', 'tag_text': '#RedRanger #Whitby42 #ICW'}, {'date': '2013-11-18 15:30:00', 'title': 'Anchor Follies', 'underline': '--------------', 'rst_text': 'Some witty epigram. Including < & > characters.', 'tag_text': '#RedRanger #Whitby42 #Mistakes'}]}
        
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
