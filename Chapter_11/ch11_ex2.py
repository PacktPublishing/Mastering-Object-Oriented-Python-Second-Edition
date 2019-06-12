#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 11. Example 2.
"""

from typing import List, Dict, Any, Optional, cast, Iterator, Union, TextIO
import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Application Classes
# ====================

# Designed to be used separately.

@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
    underline: str = field(init=False)
    tag_text: str = field(init=False)

    # Will be set as part of saving to the shelf.
    # Part of the persistence, not essential to the class.
    _id: str = field(default='', init=False, repr=False, compare=False)
    _blog_id: str = field(default='', init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "-" * len(self.title)
        self.tag_text = " ".join(self.tags)

@dataclass
class Blog:

    title: str
    underline: str = field(init=False)

    # Will be set as part of saving to the shelf.
    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)

    def by_tag(self, access: 'Access') -> Dict[str, List[Dict[str, Any]]]:
        tag_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in access.post_iter(self):
            if post._blog_id == self._id:
                for tag in post.tags:
                    tag_index[tag].append(asdict(post))
        return tag_index


test_relational_1 = """
    >>> b1 = Blog(title="Travel Blog")
    
    >>> p2 = Post(date=datetime.datetime(2013,11,14,17,25), 
    ...        title="Hard Aground", 
    ...        rst_text="Some embarrassing revelation. Including ☹ and ⚓", 
    ...        tags=("#RedRanger", "#Whitby42", "#ICW"), 
    ...        ) 
 
    >>> p3 = Post(date=datetime.datetime(2013,11,18,15,30), 
    ...        title="Anchor Follies", 
    ...        rst_text="Some witty epigram. Including < & > characters.", 
    ...        tags=("#RedRanger", "#Whitby42", "#Mistakes"), 
    ...        ) 

    >>> import shelve
    >>> from pathlib import Path
    >>> path = Path.cwd() / "data" / "ch11_blog2"
    >>> shelf = shelve.open(str(path), 'n')
    
    >>> b1._id = 'Blog:1'
    >>> shelf[b1._id] = b1
    >>> list(shelf.keys())
    ['Blog:1']
    
    >>> owner = shelf['Blog:1'] 
    >>> owner
    Blog(title='Travel Blog', underline='===========', _id='Blog:1')
    
    >>> p2._parent = owner._id 
    >>> p2._id = p2._parent + ':Post:2' 
    >>> shelf[p2._id]= p2 
     
    >>> p3._parent = owner._id 
    >>> p3._id = p3._parent + ':Post:3' 
    >>> shelf[p3._id]= p3 
    
    >>> shelf.sync()

    >>> sorted(shelf.keys())
    ['Blog:1', 'Blog:1:Post:2', 'Blog:1:Post:3']
"""

# "Relational" Access Layer -- Separate Blogs from Posts
# ======================================================

# We'll use hierarchical keys Post:id and Post:id:Child:id
import shelve


class OperationError(Exception):
    pass


class Access:

    def __init__(self) -> None:
        self.database: shelve.Shelf = cast(shelve.Shelf, None)
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}

    def new(self, path: Path) -> None:
        self.database: shelve.Shelf = shelve.open(str(path), "n")
        self.max: Dict[str, int] = {"Post": 0, "Blog": 0}
        self.sync()

    def open(self, path: Path) -> None:
        self.database = shelve.open(str(path), "w")
        self.max = self.database["_DB:max"]

    def close(self) -> None:
        if self.database:
            self.database["_DB:max"] = self.max
            self.database.close()
        self.database = cast(shelve.Shelf, None)

    def sync(self) -> None:
        self.database["_DB:max"] = self.max
        self.database.sync()

    def create_blog(self, blog: Blog) -> Blog:
        self.max['Blog'] += 1
        key = f"Blog:{self.max['Blog']}"
        blog._id = key
        self.database[blog._id] = blog
        return blog

    def retrieve_blog(self, key: str) -> Blog:
        return self.database[key]

    def create_post(self, blog: Blog, post: Post) -> Post:
        self.max['Post'] += 1
        post_key = f"Post:{self.max['Post']}"
        post._id = post_key
        post._blog_id = blog._id
        self.database[post._id] = post
        return post

    def retrieve_post(self, key: str) -> Post:
        return self.database[key]

    def update_post(self, post: Post) -> Post:
        self.database[post._id] = post
        return post

    def delete_post(self, post: Post) -> None:
        del self.database[post._id]

    def __iter__(self) -> Iterator[Union[Blog, Post]]:
        for k in self.database:
            if k[0] == "_":
                # Skip the administrative objects
                continue
            yield self.database[k]

    def blog_iter(self) -> Iterator[Blog]:
        for k in self.database:
            if k.startswith('Blog:'):
                yield self.database[k]

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        for k in self.database:
            if k.startswith('Post:'):
                if self.database[k]._blog_id == blog._id:
                    yield self.database[k]

    def post_title_iter(self, blog: Blog, title: str) -> Iterator[Post]:
        return (p for p in self.post_iter(blog) if p.title == title)

    def blog_title_iter(self, title: str) -> Iterator[Blog]:
        return (b for b in self.blog_iter() if b.title == title)


# Demonstration Script
from contextlib import closing

def database_script(access: Access) -> None:
    b1 = Blog(title="Travel Blog")
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
    access.create_blog(b1)
    for post in p2, p3:
        access.create_post(b1, post)

    b = access.retrieve_blog(b1._id)
    print(b._id, b)
    for p in sorted(access.post_iter(b), key=lambda p: p._id):
        print(p._id, p)

test_access = """
    >>> with closing(Access()) as access:
    ...     access.new(Path.cwd() / "data" / "ch11_blog")
    ...     database_script(access)
    Blog:1 Blog(title='Travel Blog', underline='===========', _id='Blog:1')
    Post:1 Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW'], underline='------------', tag_text='#RedRanger #Whitby42 #ICW')
    Post:2 Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including ☺ and ☀︎︎', tags=['#RedRanger', '#Whitby42', '#Mistakes'], underline='--------------', tag_text='#RedRanger #Whitby42 #Mistakes')
"""

# Another Application
# ==============================


import string
from collections import defaultdict
from contextlib import redirect_stdout
import sys

class Render:

    def __init__(self, access: Access) -> None:
        self.access = access

    def emit_all(self, destination: TextIO=sys.stdout) -> None:
        for blog in self.access.blog_iter():
            # Compute a filename for each blog.
            self.emit_blog(blog, destination)

    def emit_blog(self, blog: Blog, output: TextIO) -> None:
        with redirect_stdout(output):
            self.tag_index: Dict[str, List[str]] = defaultdict(list)
            print("{title}\n{underline}\n".format(**asdict(blog)))
            for post in self.access.post_iter(blog):
                self.emit_post(post)
                for tag in post.tags:
                    self.tag_index[tag].append(post._id)
            self.emit_index()

    def emit_post(self, post: Post) -> None:
        template = string.Template(
            """
        $title
        $underline

        $rst_text

        :date: $date

        :tags: $tag_text
        """
        )
        print(template.substitute(asdict(post)))

    def emit_index(self) -> None:
        print("Tag Index")
        print("=========")
        print()
        for tag in self.tag_index:
            print("*   {0}".format(tag))
            print()
            for b in self.tag_index[tag]:
                post = self.access.retrieve_post(b)
                print("    -   `{title}`_".format(**asdict(post)))
            print()


# Demo Script
import shelve
from contextlib import closing

if __name__ == "__main__":
    with closing(Access()) as access:
        access.open(Path.cwd() / "data" / "ch11_blog")
        renderer = Render(access)
        renderer.emit_all()


# Better Access Layer
# ======================================

# Maintain a indexes associated with the Blog


class Access2(Access):

    def create_post(self, blog: Blog, post: Post) -> Post:
        super().create_post(blog, post)
        # Update the index; append doesn't work.
        blog_index = f"_Index:{blog._id}"
        self.database.setdefault(blog_index, [])
        self.database[blog_index] = self.database[blog_index] + [post._id]
        return post

    def delete_post(self, post: Post) -> None:
        super().delete_post(post)
        # Update the index
        blog_index = f"_Index:{post._blog_id}"
        index_list = self.database[post._blog_id]
        index_list.remove(post._id)
        self.database[post._blog_id] = index_list

    def post_iter(self, blog: Blog) -> Iterator[Post]:
        blog_index = f"_Index:{blog._id}"
        for k in self.database[blog_index]:
            yield self.database[k]


test_access_2 = """
    >>> with closing(Access2()) as access:
    ...     access.new(Path.cwd() / "data" / "ch11_blog2")
    ...     database_script(access)
    Blog:1 Blog(title='Travel Blog', underline='===========', _id='Blog:1')
    Post:1 Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW'], underline='------------', tag_text='#RedRanger #Whitby42 #ICW')
    Post:2 Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including ☺ and ☀︎︎', tags=['#RedRanger', '#Whitby42', '#Mistakes'], underline='--------------', tag_text='#RedRanger #Whitby42 #Mistakes')

    >>> with closing(Access2()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog2")
    ...     print(sorted(access.database.keys()))
    ...     print(access.database['_Index:Blog:1'])
    ['Blog:1', 'Post:1', 'Post:2', '_DB:max', '_Index:Blog:1']
    ['Post:1', 'Post:2']
    
    
    >>> with closing(Access2()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog2")
    ...     renderer = Render(access)
    ...     renderer.emit_all()
"""

# Minor Index
# ==========================

# Another version of Access with slightly different blog add and search.
# This a tiny help, because the iteration over the cached blog keys
# is slightly faster.

class Access3(Access2):

    def new(self, path: Path) -> None:
        super().new(path)
        self.database["_Index:Blog"] = list()

    def create_blog(self, blog: Blog) -> Blog:
        super().create_blog(blog)
        self.database["_Index:Blog"] += [blog._id]
        return blog

    def blog_iter(self) -> Iterator[Blog]:
        return (self.database[k] for k in self.database["_Index:Blog"])


test_access_3 = """
    >>> with closing(Access3()) as access:
    ...     access.new(Path.cwd() / "data" / "ch11_blog3")
    ...     database_script(access)
    Blog:1 Blog(title='Travel Blog', underline='===========', _id='Blog:1')
    Post:1 Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW'], underline='------------', tag_text='#RedRanger #Whitby42 #ICW')
    Post:2 Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including ☺ and ☀︎︎', tags=['#RedRanger', '#Whitby42', '#Mistakes'], underline='--------------', tag_text='#RedRanger #Whitby42 #Mistakes')

    >>> with closing(Access3()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog3")
    ...     print(sorted(access.database.keys()))
    ...     print(access.database['_Index:Blog:1'])
    ['Blog:1', 'Post:1', 'Post:2', '_DB:max', '_Index:Blog', '_Index:Blog:1']
    ['Post:1', 'Post:2']


    >>> with closing(Access3()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog3")
    ...     renderer = Render(access)
    ...     renderer.emit_all()
"""


# Additional Indices
# ================================

# A class with multiple indices.
# Is this really worth the extra complexity?
class Access4(Access3):

    def new(self, path: Path) -> None:
        super().new(path)
        self.database["_Index:Blog_Title"] = dict()

    def create_blog(self, blog):
        super().create_blog(blog)
        blog_title_dict = self.database["_Index:Blog_Title"]
        blog_title_dict.setdefault(blog.title, [])
        blog_title_dict[blog.title].append(blog._id)
        self.database["_Index:Blog_Title"] = blog_title_dict
        return blog

    def update_blog(self, blog: Blog) -> Blog:
        """Replace this Blog; update index."""
        self.database[blog._id] = blog
        blog_title = self.database["_Index:Blog_Title"]
        # Remove key from index in old spot.
        empties = []
        for k in blog_title:
            if blog._id in blog_title[k]:
                blog_title[k].remove(blog._id)
                if len(blog_title[k]) == 0:
                    empties.append(k)
        # Cleanup zero-length lists from defaultdict.
        for k in empties:
            del blog_title[k]
        # Put key into index in new spot.
        blog_title[blog.title].append(blog._id)
        self.database["_Index:Blog_Title"] = blog_title
        return blog

    def blog_iter(self) -> Iterator[Blog]:
        return (self.database[k] for k in self.database["_Index:Blog"])

    def blog_title_iter(self, title: str) -> Iterator[Blog]:
        blog_title = self.database["_Index:Blog_Title"]
        return (self.database[k] for k in blog_title[title])


test_access_4 = """
    >>> with closing(Access4()) as access:
    ...     access.new(Path.cwd() / "data" / "ch11_blog4")
    ...     database_script(access)
    Blog:1 Blog(title='Travel Blog', underline='===========', _id='Blog:1')
    Post:1 Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW'], underline='------------', tag_text='#RedRanger #Whitby42 #ICW')
    Post:2 Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including ☺ and ☀︎︎', tags=['#RedRanger', '#Whitby42', '#Mistakes'], underline='--------------', tag_text='#RedRanger #Whitby42 #Mistakes')

    >>> with closing(Access4()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog4")
    ...     print(sorted(access.database.keys()))
    ...     print(access.database['_Index:Blog:1'])
    ['Blog:1', 'Post:1', 'Post:2', '_DB:max', '_Index:Blog', '_Index:Blog:1', '_Index:Blog_Title']
    ['Post:1', 'Post:2']


    >>> with closing(Access4()) as access:
    ...     access.open(Path.cwd() / "data" / "ch11_blog4")
    ...     renderer = Render(access)
    ...     renderer.emit_all()
"""


# Timing Comparison
# ================================

# Larger Database Required
import time
import io


def create(access, blogs=100, posts_per_blog=100) -> None:
    for b_n in range(blogs):
        b = Blog("Blog {0}".format(b_n))
        access.create_blog(b)
        for p_n in range(posts_per_blog):
            p = Post(
                date=datetime.datetime.now(),
                title="Blog {0}; Post {1}".format(b_n, p_n),
                rst_text="Blog {0}; Post {1}\nText\n".format(b_n, p_n),
                tags=list("#tag{0}".format(p_n + i) for i in range(3)),
            )
            access.create_post(b, p)


def performance(cycles=3):
    import random

    result: Dict[str, float] = defaultdict(int)
    base_path = Path.cwd() / "data"

    for filename, class_ in (
        (base_path / "ch11_blog_t", Access),
        (base_path / "ch11_blog_t2", Access2),
        (base_path / "ch11_blog_t3", Access3),
        (base_path / "ch11_blog_t4", Access4),
    ):

        buffer = io.StringIO()
        start = time.perf_counter()
        for _ in range(cycles):
            with closing(class_()) as access:
                access.new(filename)
                create(access, blogs=100, posts_per_blog=100)
            with closing(class_()) as access:
                access.open(filename)
                renderer = Render(access)
                renderer.emit_all(buffer)
            with closing(class_()) as access:
                access.open(filename)
                renderer = Render(access)
                titles = []
                for i in range(10):
                    choice = random.randint(1, 100)
                    blog_by_id = access.retrieve_blog(f"Blog:{choice}")
                    renderer.emit_blog(blog_by_id, buffer)
                    titles.append(blog_by_id.title)
            with closing(class_()) as access:
                access.open(filename)
                renderer = Render(access)
                for t in titles:
                    blogs = access.blog_title_iter(t)
                    for b in blogs:
                        renderer.emit_blog(b, buffer)
        finish = time.perf_counter()
        result[class_.__name__] = finish - start

    print("Time to create and render 10,000 posts")
    for r in sorted(result):
        print(
            f"Access Layer {r}: {result[r]/cycles:.1f} seconds "
        )

    for path in base_path.glob("ch11_blog_t*.*"):
        path.unlink()


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    # performance()   # Takes 45 seconds

"""
Time to create and render 10,000 posts
Access Layer Access: 33.5 seconds 
Access Layer Access2: 4.0 seconds 
Access Layer Access3: 3.9 seconds 
Access Layer Access4: 4.0 seconds 
"""