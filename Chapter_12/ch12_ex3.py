#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 12. Example 3.
"""

# Manual ORM
# =========================

from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, DefaultDict, Optional, Iterator, cast
import sqlite3
import datetime
from contextlib import closing
from collections import defaultdict
from weakref import ref


@dataclass
class Blog:

    title: str
    underline: str = field(init=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)
    _access: Optional[ref] = field(init=False, repr=False, default=None, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)

    @property
    def entries(self) -> List['Post']:
        if self._access and self._access():
            posts = cast('Access', self._access()).post_iter(self)
            return list(posts)
        raise RuntimeError("Can't work with Blog: no associated Access instance")

    def by_tag(self) -> Dict[str, List[Dict[str, Any]]]:
        if self._access and self._access():
            return cast('Access', self._access()).post_by_tag(self)
        raise RuntimeError("Can't work with Blog: no associated Access instance")

@dataclass
class Post:

    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str] = field(default_factory=list)
    _id: str = field(default="", init=False, compare=False)

    def append(self, tag):
        self.tags.append(tag)


# An access layer to map back and forth between Python objects and SQL rows.
class Access:
    get_last_id = """
        SELECT last_insert_rowid()
    """

    def open(self, path: Path) -> None:
        self.database = sqlite3.connect(path)
        self.database.row_factory = sqlite3.Row

    def get_blog(self, id: str) -> Blog:
        query_blog = """
            SELECT * FROM blog WHERE id=?
        """
        row = self.database.execute(query_blog, (id,)).fetchone()
        blog = Blog(title=row["TITLE"])
        blog._id = row["ID"]
        blog._access = ref(self)
        return blog

    def add_blog(self, blog: Blog) -> Blog:
        insert_blog = """
            INSERT INTO blog(title) VALUES(:title)
        """
        self.database.execute(insert_blog, dict(title=blog.title))
        row = self.database.execute(self.get_last_id).fetchone()
        blog._id = str(row[0])
        blog._access = ref(self)
        return blog

    def get_post(self, id: str) -> Post:
        query_post = """
            SELECT * FROM post WHERE id=?
        """
        row = self.database.execute(query_post, (id,)).fetchone()
        post = Post(
            title=row["TITLE"], date=row["DATE"], rst_text=row["RST_TEXT"]
        )
        post._id = row["ID"]
        # Get tag text, too
        query_tags = """
            SELECT tag.*
            FROM tag JOIN assoc_post_tag ON tag.id = assoc_post_tag.tag_id
            WHERE assoc_post_tag.post_id=?
        """
        results = self.database.execute(query_tags, (id,))
        for tag_id, phrase in results:
            post.append(phrase)
        return post

    def add_post(self, blog: Blog, post: Post) -> Post:
        insert_post = """
            INSERT INTO post(title, date, rst_text, blog_id) VALUES(:title, :date, :rst_text, :blog_id)
        """
        query_tag = """
            SELECT * FROM tag WHERE phrase=?
        """
        insert_tag = """
            INSERT INTO tag(phrase) VALUES(?)
        """
        insert_association = """
            INSERT INTO assoc_post_tag(post_id, tag_id) VALUES(:post_id, :tag_id)
        """
        try:
            with closing(self.database.cursor()) as cursor:
                cursor.execute(
                    insert_post,
                    dict(
                        title=post.title,
                        date=post.date,
                        rst_text=post.rst_text,
                        blog_id=blog._id,
                    ),
                )
                row = cursor.execute(self.get_last_id).fetchone()
                post._id = str(row[0])
                for tag in post.tags:
                    tag_row = cursor.execute(query_tag, (tag,)).fetchone()
                    if tag_row is not None:
                        tag_id = tag_row["ID"]
                    else:
                        cursor.execute(insert_tag, (tag,))
                        row = cursor.execute(self.get_last_id).fetchone()
                        tag_id = str(row[0])
                    cursor.execute(
                        insert_association,
                        dict(tag_id=tag_id, post_id=post._id)
                    )
            self.database.commit()
        except Exception as ex:
            self.database.rollback()
            raise
        return post

    def blog_iter(self) -> Iterator[Blog]:
        query = """
            SELECT * FROM blog
        """
        results = self.database.execute(query)
        for row in results:
            blog = Blog(title=row["TITLE"])
            blog._id = row["ID"]
            blog._access = ref(self)
            yield blog

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        query = """
            SELECT id FROM post WHERE blog_id=?
        """
        results = self.database.execute(query, (blog._id,))
        for row in results:
            yield self.get_post(row["ID"])

    def post_by_tag(self, blog: Blog) -> Dict[str, List[Dict[str, Any]]]:
        """All posts of a blog, organized by tag, represented as dictionaries."""
        query_by_tag = """ 
            SELECT tag.phrase, post.id
            FROM tag JOIN assoc_post_tag ON tag.id = assoc_post_tag.tag_id 
            JOIN post ON post.id = assoc_post_tag.post_id 
            JOIN blog ON post.blog_id = blog.id 
            WHERE blog.title=? 
        """
        results = self.database.execute(query_by_tag, (blog.title,))
        tags: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for phrase, post_id in results.fetchall():
            tags[phrase].append(asdict(self.get_post(post_id)))
        return tags


if __name__ == "__main__":
    database_access = Access()
    database_access.open(Path.cwd() / "data" / "ch12_blog.db")
    b = Blog(title="2012 Travel")
    database_access.add_blog(b)
    print(b._id)
    p = Post(
        title="Some History",
        date=datetime.datetime(2012, 9, 16, 10, 00),
        rst_text="Some historyical notes.",
        tags=["#History", "#RedRanger"],
    )
    database_access.add_post(b, p)

    d = b.by_tag()
    print(d)

    for b in database_access.blog_iter():
        # print(f"b = {iter(b)}")
        print(asdict(b))
        for p in database_access.post_iter(b):
            print(asdict(p))

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
