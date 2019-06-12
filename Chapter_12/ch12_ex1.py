#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 12. Example 1.
"""

from typing import Dict, List, Tuple

# One issue here is that the microblog has no processing.
# The classes tend to be rather anemic.

# The upside is that it has all of the relevant relationships
# So it shows SQL key handling nicely.

# SQL Basics
# ========================================

# Some Example Table Declarations for a simple microblog.
sql_cleanup = """
DROP TABLE IF EXISTS blog;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS assoc_post_tag;
"""

sql_ddl = """
CREATE TABLE blog(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT 
);
CREATE TABLE post(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP,
    title TEXT,
    rst_text TEXT,
    blog_id INTEGER REFERENCES blog(id)
);
CREATE TABLE tag(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phrase TEXT UNIQUE ON CONFLICT FAIL
);
CREATE TABLE assoc_post_tag(
    post_id INTEGER REFERENCES post(id),
    tag_id INTEGER REFERENCES tag(id)
);
"""

import sqlite3
from pathlib import Path
from contextlib import closing

database = sqlite3.connect(Path.cwd() / "data" / "ch12_blog.db")  # type: ignore
# Note that sqlite3 really does use a Path. The declaration doesn't include it.
# We have two choices.
# 1. Use a ``# typing: ignore`` comment
# 2. use ``str(Path.cwd()/"data"/"ch12_blog.db")``

# reveal_type(sqlite3.connect)

database.executescript(sql_cleanup)

with closing(database.cursor()) as cursor:
    for stmt in (stmt.rstrip() for stmt in sql_ddl.split(";")):
        print(stmt)
        cursor.execute(stmt)
        print(cursor)
database.commit()
database.close()

# ACID
# ===============

database = sqlite3.connect(
    Path.cwd() / "data" / "ch12_blog.db", isolation_level="DEFERRED"
)  # type: ignore
try:
    with closing(database.cursor()) as cursor:
        cursor.execute("BEGIN")
        # cursor.execute("some statement")
        # cursor.execute("another statement")
    database.commit()
except Exception as e:
    database.rollback()

# Simple SQL
# ======================

# Import
import datetime

# Connection
database = sqlite3.connect(Path.cwd() / "data" / "ch12_blog.db")  # type: ignore

# Useful query to figuring out what PK was automatically assigned.
get_last_id = """
SELECT last_insert_rowid()
"""

with closing(database.cursor()) as cursor:
    cursor.execute("BEGIN")

    # Build BLOG
    create_blog = """
        INSERT INTO blog(title) VALUES(?)
    """
    cursor.execute(create_blog, ("Travel Blog",))
    row = cursor.execute(get_last_id).fetchone()
    blog_id = row[0]

    # Build POST
    create_post = """
        INSERT INTO post(date, title, rst_text, blog_id) VALUES(?, ?, ?, ?)
    """
    cursor.execute(
        create_post,
        (
            datetime.datetime(2013, 11, 14, 17, 25),
            "Hard Aground",
            """Some embarrassing revelation. Including ☹ and ⚓︎""",
            blog_id,
        ),
    )
    row = cursor.execute(get_last_id).fetchone()
    post_id = row[0]

    # Build TAGs for a Post
    create_tag = """
        INSERT INTO tag(phrase) VALUES(?)
    """
    retrieve_tag = """
        SELECT id, phrase FROM tag WHERE phrase = ?
    """
    create_tag_post_association = """
        INSERT INTO assoc_post_tag(post_id, tag_id) VALUES (?, ?)
    """
    for tag in ("#RedRanger", "#Whitby42", "#ICW"):
        row = cursor.execute(retrieve_tag, (tag,)).fetchone()
        if row:
            tag_id = row[0]
        else:
            cursor.execute(create_tag, (tag,))
            row = cursor.execute(get_last_id).fetchone()
            tag_id = row[0]
        cursor.execute(create_tag_post_association, (post_id, tag_id))

database.commit()

update_blog = """
    UPDATE blog SET title=:new_title WHERE title=:old_title
"""
with closing(database.cursor()) as cursor:
    # Sample Update
    cursor.execute("BEGIN")
    cursor.execute(
        update_blog,
        dict(
            new_title="2013-2014 Travel",
            old_title="Travel Blog")
    )
database.commit()

# Sample Delete
delete_post_tag_by_blog_title = """
    DELETE FROM assoc_post_tag
    WHERE post_id IN (
        SELECT DISTINCT post_id
        FROM blog JOIN post ON blog.id = post.blog_id
        WHERE blog.title=:old_title)
"""
delete_post_by_blog_title = """
    DELETE FROM post WHERE blog_id IN (
        SELECT id FROM blog WHERE title=:old_title)
"""
delete_blog_by_title = """
    DELETE FROM blog WHERE title=:old_title
"""
try:
    with closing(database.cursor()) as cursor:
        title = dict(old_title="2013-2014 Travel")
        cursor.execute("BEGIN")
        cursor.execute(delete_post_tag_by_blog_title, title)
        cursor.execute(delete_post_by_blog_title, title)
        cursor.execute(delete_blog_by_title, title)
        print("Post Delete, Pre Commit; should be no '2013-2014 Travel'")
        cursor.execute("SELECT * FROM blog")
        for row in cursor.fetchall():
            print(row)
        cursor.execute("SELECT * FROM post")
        for row in cursor.fetchall():
            print(row)
        cursor.execute("SELECT * FROM assoc_post_tag")
        for row in cursor.fetchall():
            print(row)
        raise Exception("Demonstrating an Error")
    print("Should not get here to commit.")
    database.commit()
except Exception as ex:
    print(f"Rollback due to {ex!r}")
    database.rollback()

# Bulk examination of database to show simple queries
with closing(database.cursor()) as cursor:
    print("Dumping whole database.")
    for row in cursor.execute("SELECT * FROM blog"):
        print("BLOG", row)
    for row in cursor.execute("SELECT * FROM post"):
        print("POST", row)
    for row in cursor.execute("SELECT * FROM tag"):
        print("TAG", row)
    for row in cursor.execute(
        """
        SELECT assoc_post_tag.* 
        FROM post 
            JOIN assoc_post_tag ON post.id=assoc_post_tag.post_id 
            JOIN tag ON tag.id=assoc_post_tag.tag_id
        """
    ):
        print("ASSOC_POST_TAG", row)

# Naked SQL Query
# ==========================

print("Dump a single blog by title.")

# Three-step nested queries
query_blog_by_title = """
SELECT * FROM blog WHERE title=?
"""
query_post_by_blog_id = """
SELECT * FROM post WHERE blog_id=?
"""
query_tag_by_post_id = """
SELECT tag.*
FROM tag JOIN assoc_post_tag ON tag.id = assoc_post_tag.tag_id
WHERE assoc_post_tag.post_id=?
"""
with closing(database.cursor()) as blog_cursor:
    blog_cursor.execute(query_blog_by_title, ("2013-2014 Travel",))
    for blog in blog_cursor.fetchall():
        print("Blog", blog)
        with closing(database.cursor()) as post_cursor:
            post_cursor.execute(query_post_by_blog_id, (blog[0],))
            for post in post_cursor:
                print("Post", post)
                with closing(database.cursor()) as tag_cursor:
                    tag_cursor.execute(query_tag_by_post_id, (post[0],))
                    for tag in tag_cursor.fetchall():
                        print("Tag", tag)

# Tag index
from collections import defaultdict

query_by_tag = """
    SELECT tag.phrase, post.title, post.id
    FROM tag JOIN assoc_post_tag ON tag.id = assoc_post_tag.tag_id
    JOIN post ON post.id = assoc_post_tag.post_id
    JOIN blog ON post.blog_id = blog.id
    WHERE blog.title=?
"""
tag_index: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
with closing(database.cursor()) as cursor:
    cursor.execute(query_by_tag, ("2013-2014 Travel",))
    for tag, post_title, post_id in cursor.fetchall():
        tag_index[tag].append((post_title, post_id))
    print(tag_index)

database.close()

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
