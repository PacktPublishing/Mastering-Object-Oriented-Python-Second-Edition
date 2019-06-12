#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 17. Example 2.
"""
import unittest


# SQLite testing
# =========================

# This is integration testing, not unit testing.
# Integration means we use the database
# instead of isolating our code from the database.
# A more formal unit test would mock the database layer.


# SQLAlchemy ORM classes

from typing import Any
from Chapter_12.ch12_ex4 import Base, Blog, Post, Tag, assoc_post_tag
import datetime


import sqlalchemy.exc
from sqlalchemy import create_engine


def build_test_db(name="sqlite:///./data/ch17_blog.db"):
    """
    Create Test Database and Schema
    """
    engine = create_engine(name, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine


# Unittest Case

from sqlalchemy.orm import sessionmaker, Session


class Test_Blog_Queries(unittest.TestCase):

    Session: Any
    session: Session

    @staticmethod
    def setUpClass() -> None:
        engine = build_test_db()
        Test_Blog_Queries.Session = sessionmaker(bind=engine)
        session = Test_Blog_Queries.Session()

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

    def setUp(self) -> None:
        self.session = Test_Blog_Queries.Session()

    def test_query_eqTitle_should_return1Blog(self) -> None:
        """Tests schema definition"""
        results = self.session.query(Blog).filter(Blog.title == "Travel 2013").all()
        self.assertEqual(1, len(results))
        self.assertEqual(2, len(results[0].entries))

    def test_query_likeTitle_should_return2Blog(self) -> None:
        """Tests SQLAlchemy, and test data"""
        results = self.session.query(Blog).filter(Blog.title.like("Travel %")).all()
        self.assertEqual(2, len(results))

    def test_query_eqW42_tag_should_return2Post(self) -> None:
        results = self.session.query(Post).join(assoc_post_tag).join(Tag).filter(
            Tag.phrase == "#Whitby42"
        ).all()
        self.assertEqual(2, len(results))

    def test_query_eqICW_tag_should_return1Post(self) -> None:
        results = self.session.query(Post).join(assoc_post_tag).join(Tag).filter(
            Tag.phrase == "#ICW"
        ).all()
        # print( [r.title for r in results] )
        self.assertEqual(1, len(results))
        self.assertEqual("Hard Aground", results[0].title)
        self.assertEqual("Travel 2013", results[0].blog.title)
        self.assertEqual(
            set(["#RedRanger", "#Whitby42", "#ICW"]),
            set(t.phrase for t in results[0].tags),
        )


# Make a suite of the testcases


def suite8() -> unittest.TestSuite:
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Blog_Queries))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite8())

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
