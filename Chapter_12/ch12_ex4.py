#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 12. Example 4.

..  important::

    SQLAlchemy doesn't include any stubs or type hints.

    There's no point in running mypy on this module. You'll see the following
    errors (plus a few others)::

        Chapter_12/ch12_ex4.py:18: error: No library stub file for module 'sqlalchemy.ext.declarative'
        Chapter_12/ch12_ex4.py:18: note: (Stub files are from https://github.com/python/typeshed)
        Chapter_12/ch12_ex4.py:23: error: No library stub file for module 'sqlalchemy'
        Chapter_12/ch12_ex4.py:44: error: No library stub file for module 'sqlalchemy.orm'
        Chapter_12/ch12_ex4.py:117: error: No library stub file for module 'sqlalchemy.exc'

"""

import datetime

# SQLAlchemy Mapping
# ==============================

# Some Classes that reflect our SQL data.
from sqlalchemy.ext.declarative import declarative_base

# Section 3.2.5 lists the column types
from sqlalchemy import Column, Table
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    PickleType,
    SmallInteger,
    String,
    Text,
    Time,
    Unicode,
    UnicodeText,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

# There are standard types and vendor types, also.
# We'll stick with generic types.

# The metaclass
Base = declarative_base()

# The application class/table declarations
class Blog(Base):
    __tablename__ = "BLOG"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def as_dict(self):
        return dict(
            title=self.title,
            underline="=" * len(self.title),
            entries=[e.as_dict() for e in self.entries],
        )


assoc_post_tag = Table(
    "ASSOC_POST_TAG",
    Base.metadata,
    Column("POST_ID", Integer, ForeignKey("POST.id")),
    Column("TAG_ID", Integer, ForeignKey("TAG.id")),
)


class Post(Base):
    __tablename__ = "POST"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(DateTime)
    rst_text = Column(UnicodeText)
    blog_id = Column(Integer, ForeignKey("BLOG.id"))
    blog = relationship("Blog", backref="entries")
    tags = relationship("Tag", secondary=assoc_post_tag, backref="posts")

    def as_dict(self):
        return dict(
            title=self.title,
            underline="-" * len(self.title),
            date=self.date,
            rst_text=self.rst_text,
            tags=[t.phrase for t in self.tags],
        )


class Tag(Base):
    __tablename__ = "TAG"
    id = Column(Integer, primary_key=True)
    phrase = Column(String, unique=True)


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)

    # Building a schema
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///./data/ch12_blog2.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Loading some data
    import sqlalchemy.exc
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)

    session = Session()

    blog = Blog(title="Travel 2013")
    session.add(blog)

    tags = []
    for phrase in "#RedRanger", "#Whitby42", "#ICW":
        try:
            tag = session.query(Tag).filter(Tag.phrase == phrase).one()
        except sqlalchemy.orm.exc.NoResultFound:
            tag = Tag(phrase=phrase)
            session.add(tag)
        tags.append(tag)

    p2 = Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓︎""",
        blog=blog,
        tags=tags,
    )
    session.add(p2)

    tags = []
    for phrase in "#RedRanger", "#Whitby42", "#Mistakes":
        try:
            tag = session.query(Tag).filter(Tag.phrase == phrase).one()
        except sqlalchemy.orm.exc.NoResultFound:
            tag = Tag(phrase=phrase)
            session.add(tag)
        tags.append(tag)

    p3 = Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including ☺ and ☀︎︎""",
        blog=blog,
        tags=tags,
    )
    session.add(p3)
    blog.posts = [p2, p3]

    session.commit()

    session = Session()

    for blog in session.query(Blog):
        print("{title}\n{underline}\n".format(**blog.as_dict()))
        for p in blog.entries:
            print(p.as_dict())

    session2 = Session()
    results = (
        session2.query(Post).join(assoc_post_tag).join(Tag).filter(
            Tag.phrase == "#Whitby42"
        )
    )
    for post in results:
        print(post.blog.title, post.date, post.title, [t.phrase for t in post.tags])
