#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 11. Example 1.
"""


# Shelve Basics
# ========================================

from typing import List, Dict, Any, Optional
from collections import defaultdict
import datetime
from pathlib import Path
from dataclasses import dataclass, asdict, field
import shelve


# Some Example Application Classes


@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]


@dataclass
class Blog:

    title: str
    entries: List[Post] = field(default_factory=list)
    underline: str = field(init=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)

    def append(self, post: Post) -> None:
        self.entries.append(post)

    def by_tag(self) -> Dict[str, List[Dict[str, Any]]]:
        tag_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self.entries:
            for tag in post.tags:
                tag_index[tag].append(asdict(post))
        return tag_index

test_blog = """
    >>> b1 = Blog(title="Travel Blog")
    >>> b1
    Blog(title='Travel Blog', entries=[], underline='===========', _id='')

    >>> import shelve
    >>> from pathlib import Path
    >>> path = Path.cwd() / "data" / "ch11_blog1"
    >>> shelf = shelve.open(str(path), "n")
    >>> b1._id = 'Blog:1'
    >>> shelf[b1._id] = b1
    
    >>> shelf['Blog:1']
    Blog(title='Travel Blog', entries=[], underline='===========', _id='Blog:1')
    >>> shelf['Blog:1'].title 
    'Travel Blog'
    >>> shelf['Blog:1']._id 
    'Blog:1'
    >>> list(shelf.keys()) 
    ['Blog:1']
    >>> shelf.close() 
"""

test_query = """
    >>> path = Path.cwd() / "data" / "ch11_blog1"
    >>> shelf = shelve.open(str(path))
    >>> results = (shelf[k] 
    ...     for k in shelf.keys() 
    ...     if k.startswith('Blog:') and shelf[k].title == 'Travel Blog'
    ... )
    >>> list(results)
    [Blog(title='Travel Blog', entries=[], underline='===========', _id='Blog:1')]
"""

if __name__ == "__main__":
    # A Blog example
    b1 = Blog(title="Travel Blog")
    p1 = Post(
        date=datetime.datetime(2019, 1, 18),
        title="Some Post",
        rst_text="Details of the post",
        tags=["#sample", "#data"],
    )
    b1.append(p1)

    # Some Manual access
    import shelve

    shelf = shelve.open(str(Path.cwd() / "data" / "ch11_blog"))
    db_id = 0

    # Typical seqence for saving...
    db_id += 1
    b1._id = f"Blog:{db_id}"
    shelf[b1._id] = b1
    print(f"Create {shelf[b1._id]._id} {shelf[b1._id].title}")

    # Seaching through the shelf for a specific title...
    results = (
        shelf[k]
        for k in shelf.keys()
        if k.startswith("Blog:") and shelf[k].title == "Travel Blog"
    )
    for r0 in results:
        print(f"Retrieve {r0._id} {r0.title}")
        for p in r0.entries:
            print(f"  {p}")
        print(f"  {r0.by_tag()}")

    shelf.close()


# Some more manual access
if __name__ == "__main__":

    p2 = Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓︎""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )

    p3 = Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including ☺ and ☀︎︎""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )

    shelf = shelve.open(str(Path.cwd() / "data" / "ch11_blog"))

    # Retrieve the blog by id
    blog_id = 1
    key = f"Blog:{blog_id}"
    the_blog = shelf[key]

    # Update the blog
    the_blog.append(p2)
    the_blog.append(p3)

    # Persist the changes to the blog.
    shelf[key] = the_blog

    # What's in the database?
    print("Database has", list(shelf.keys()))

    shelf.close()


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
