#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 1. JSON
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
from typing import List, Optional, Dict, Any, DefaultDict, Union, Type
from pathlib import Path
import datetime
from dataclasses import dataclass

# Technically, this is the type supported by JSON serailization.
# JSON = Union[Dict[str, 'JSON'], List['JSON'], int, str, float, bool, Type[None]]
JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

@dataclass
class Post:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            date=str(self.date),
            title=self.title,
            underline="-" * len(self.title),
            rst_text=self.rst_text,
            tag_text=" ".join(self.tags),
        )


# Here's a collection of these posts. This is an extension
# of list which doesn't work well with JSON.

from collections import defaultdict

class Blog_x(list):

    def __init__(self, title: str, posts: Optional[List[Post]]=None) -> None:
        self.title = title
        super().__init__(posts if posts is not None else [])

    def by_tag(self) -> DefaultDict[str, List[Dict[str, Any]]]:
        tag_index: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self:
            for tag in post.tags:
                tag_index[tag].append(post.as_dict())
        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            title=self.title,
            entries=[p.as_dict() for p in self]
        )


# An example blog
travel_x = Blog_x("Travel")
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including < & > characters.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)

# JSON
# ================================

# Example 1: Simple
# ####################

# Simple JSON dump
import json

test_json_1 = """
    >>> print(json.dumps(travel_x.as_dict(), indent=4))
    {
        "title": "Travel",
        "entries": [
            {
                "date": "2013-11-14 17:25:00",
                "title": "Hard Aground",
                "underline": "------------",
                "rst_text": "Some embarrassing revelation. Including \u2639 and \u2693",
                "tag_text": "#RedRanger #Whitby42 #ICW"
            },
            {
                "date": "2013-11-18 15:30:00",
                "title": "Anchor Follies",
                "underline": "--------------",
                "rst_text": "Some witty epigram. Including < & > characters.",
                "tag_text": "#RedRanger #Whitby42 #Mistakes"
            }
        ]
    }
    """

# Example 2. JSON: Flawed Container Design
# ########################################

# Flawed Encoder based on flawed design of the class.
def blogx_encode(object: Any) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second,
            ),
        )
    elif isinstance(object, Post):
        return dict(
            __class__="Post",
            __args__=[],
            __kw__=dict(
                date=object.date,
                title=object.title,
                rst_text=object.rst_text,
                tags=object.tags,
            ),
        )
    elif isinstance(object, Blog_x):
        # Will get ignored...
        return dict(
            __class__="Blog_x",
            __args__=[],
            __kw__=dict(title=object.title, entries=tuple(object)),
        )
    else:
        return object

def blogx_decode(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    if set(some_dict.keys()) == set(["__class__", "__args__", "__kw__"]):
        class_ = eval(some_dict["__class__"])
        return class_(*some_dict["__args__"], **some_dict["__kw__"])
    else:
        return some_dict

test_json_2 = """
    >>> text = json.dumps(travel_x, indent=4, default=blogx_encode)
    >>> print(text)
    [
        {
            "__class__": "Post",
            "__args__": [],
            "__kw__": {
                "date": {
                    "__class__": "datetime.datetime",
                    "__args__": [],
                    "__kw__": {
                        "year": 2013,
                        "month": 11,
                        "day": 14,
                        "hour": 17,
                        "minute": 25,
                        "second": 0
                    }
                },
                "title": "Hard Aground",
                "rst_text": "Some embarrassing revelation. Including \u2639 and \u2693",
                "tags": [
                    "#RedRanger",
                    "#Whitby42",
                    "#ICW"
                ]
            }
        },
        {
            "__class__": "Post",
            "__args__": [],
            "__kw__": {
                "date": {
                    "__class__": "datetime.datetime",
                    "__args__": [],
                    "__kw__": {
                        "year": 2013,
                        "month": 11,
                        "day": 18,
                        "hour": 15,
                        "minute": 30,
                        "second": 0
                    }
                },
                "title": "Anchor Follies",
                "rst_text": "Some witty epigram. Including < & > characters.",
                "tags": [
                    "#RedRanger",
                    "#Whitby42",
                    "#Mistakes"
                ]
            }
        }
    ]
        
    The Blog structure overall? Vanished. It's only a list
    >>> from pprint import pprint
    >>> copy = json.loads(text, object_hook=blogx_decode)
    >>> pprint(copy)
    [Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓', tags=['#RedRanger', '#Whitby42', '#ICW']),
     Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including < & > characters.', tags=['#RedRanger', '#Whitby42', '#Mistakes'])]

"""

# Example 3 JSON: Better Design
# ###############################

# Consider this wrap-based design instead of an extension-based version

# Here's another collection of these posts.
# This wraps a list which works much better with JSON than extending a list.

import datetime
from collections import defaultdict


class Blog:

    def __init__(self, title: str, posts: Optional[List[Post]]=None) -> None:
        self.title = title
        self.entries = posts if posts is not None else []

    @property
    def underline(self) -> str:
        return '='*len(self.title)

    def append(self, post: Post) -> None:
        self.entries.append(post)

    def by_tag(self) -> Dict[str, List[Dict[str, Any]]]:
        tag_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self.entries:
            for tag in post.tags:
                tag_index[tag].append(post.as_dict())
        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            title=self.title,
            underline=self.underline,
            entries=[p.as_dict() for p in self.entries],
        )


# An example blog
travel = Blog("Travel")
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓︎""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including < & > characters.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)


def blog_encode(object: Any) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second,
            ),
        )
    elif isinstance(object, Post):
        return dict(
            __class__="Post",
            __args__=[],
            __kw__=dict(
                date=object.date,
                title=object.title,
                rst_text=object.rst_text,
                tags=object.tags,
            ),
        )
    elif isinstance(object, Blog):
        return dict(
            __class__="Blog", __args__=[object.title, object.entries], __kw__={}
        )
    else:
        return object


def blog_decode(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    if set(some_dict.keys()) == {"__class__", "__args__", "__kw__"}:
        class_ = eval(some_dict["__class__"])
        return class_(*some_dict["__args__"], **some_dict["__kw__"])
    else:
        return some_dict


test_json_3 = """
    >>> text = json.dumps(travel, indent=4, default=blog_encode)
    >>> print(text)
    {
        "__class__": "Blog",
        "__args__": [
            "Travel",
            [
                {
                    "__class__": "Post",
                    "__args__": [],
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime",
                            "__args__": [],
                            "__kw__": {
                                "year": 2013,
                                "month": 11,
                                "day": 14,
                                "hour": 17,
                                "minute": 25,
                                "second": 0
                            }
                        },
                        "title": "Hard Aground",
                        "rst_text": "Some embarrassing revelation. Including \u2639 and \u2693\ufe0e",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#ICW"
                        ]
                    }
                },
                {
                    "__class__": "Post",
                    "__args__": [],
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime",
                            "__args__": [],
                            "__kw__": {
                                "year": 2013,
                                "month": 11,
                                "day": 18,
                                "hour": 15,
                                "minute": 30,
                                "second": 0
                            }
                        },
                        "title": "Anchor Follies",
                        "rst_text": "Some witty epigram. Including < & > characters.",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#Mistakes"
                        ]
                    }
                }
            ]
        ],
        "__kw__": {}
    }
    
    >>> from pprint import pprint
    >>> copy = json.loads(text, object_hook=blog_decode)
    >>> print(copy.title)
    Travel
    >>> pprint(copy.entries)
    [Post(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓︎', tags=['#RedRanger', '#Whitby42', '#ICW']),
     Post(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram. Including < & > characters.', tags=['#RedRanger', '#Whitby42', '#Mistakes'])]
"""

# Sidebar: Demo of rendering 1
# ###############################

# Here's a template for an individual post
import string

# Here's a way to render the entire blog in RST
def rst_render(blog: Blog) -> None:
    post = string.Template(
        """
    $title
    $underline

    $rst_text

    :date: $date

    :tags: $tag_text
    """
    )

    # with contextlib.redirect_stdout("some_file"):
    print(f"{blog.title}\n{blog.underline}\n")
    for p in blog.entries:
        print(post.substitute(**p.as_dict()))

    tag_index = blog.by_tag()
    print("Tag Index")
    print("=========")
    print()
    for tag in tag_index:
        print(f"*   {tag}")
        print()
        for post_dict in tag_index[tag]:
            print(f"    -   `{post_dict['title']}`_")
        print()

test_string_template_render = """
    >>> rst_render(travel)
    Travel
    ======
    <BLANKLINE>
    <BLANKLINE>
        Hard Aground
        ------------
    <BLANKLINE>
        Some embarrassing revelation. Including ☹ and ⚓︎
    <BLANKLINE>
        :date: 2013-11-14 17:25:00
    <BLANKLINE>
        :tags: #RedRanger #Whitby42 #ICW
    <BLANKLINE>
    <BLANKLINE>
        Anchor Follies
        --------------
    <BLANKLINE>
        Some witty epigram. Including < & > characters.
    <BLANKLINE>
        :date: 2013-11-18 15:30:00
    <BLANKLINE>
        :tags: #RedRanger #Whitby42 #Mistakes
    <BLANKLINE>
    Tag Index
    =========
    <BLANKLINE>
    *   #RedRanger
    <BLANKLINE>
        -   `Hard Aground`_
        -   `Anchor Follies`_
    <BLANKLINE>
    *   #Whitby42
    <BLANKLINE>
        -   `Hard Aground`_
        -   `Anchor Follies`_
    <BLANKLINE>
    *   #ICW
    <BLANKLINE>
        -   `Hard Aground`_
    <BLANKLINE>
    *   #Mistakes
    <BLANKLINE>
        -   `Anchor Follies`_
    <BLANKLINE>

"""

# Sidebar: Demo of rendering 2 (using Jinja2)
# ############################################

from jinja2 import Template

blog_template = Template(
"""{{title}}
{{underline}}

{% for e in entries %}
    {{e.title}}
    {{e.underline}}

    {{e.rst_text}}

    :date: {{e.date}}

    :tags: {{e.tag_text}}
    
{% endfor %}

Tag Index
=========
{% for t in tags %}
*   {{t}}
    {% for post in tags[t] %}
    -   `{{post.title}}`_
    {%- endfor %}
{% endfor %}
"""
)

test_jinja_temple_render = """
    >>> print(blog_template.render(tags=travel.by_tag(), **travel.as_dict()))
    Travel
    ======
    <BLANKLINE>
    <BLANKLINE>
        Hard Aground
        ------------
    <BLANKLINE>
        Some embarrassing revelation. Including ☹ and ⚓︎
    <BLANKLINE>
        :date: 2013-11-14 17:25:00
    <BLANKLINE>
        :tags: #RedRanger #Whitby42 #ICW
    <BLANKLINE>
    <BLANKLINE>
        Anchor Follies
        --------------
    <BLANKLINE>
        Some witty epigram. Including < & > characters.
    <BLANKLINE>
        :date: 2013-11-18 15:30:00
    <BLANKLINE>
        :tags: #RedRanger #Whitby42 #Mistakes
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    Tag Index
    =========
    <BLANKLINE>
    *   #RedRanger
    <BLANKLINE>
        -   `Hard Aground`_
        -   `Anchor Follies`_
    <BLANKLINE>
    *   #Whitby42
    <BLANKLINE>
        -   `Hard Aground`_
        -   `Anchor Follies`_
    <BLANKLINE>
    *   #ICW
    <BLANKLINE>
        -   `Hard Aground`_
    <BLANKLINE>
    *   #Mistakes
    <BLANKLINE>
        -   `Anchor Follies`_
    <BLANKLINE>
"""

# Example 4. JSON: Refactoring Encoding
# ######################################

# Changes to the class definitions to add a ``_json`` method.


class Post_J(Post):
    """Not really essential to inherit from Post, it's simply a dataclass."""
    @property
    def _json(self) -> Dict[str, Any]:
        return dict(
            __class__=self.__class__.__name__,
            __kw__=dict(
                date=self.date, title=self.title, rst_text=self.rst_text, tags=self.tags
            ),
            __args__=[],
        )

class Blog_J(Blog):
    """Note. No explicit reference to Blog_J for entries."""

    @property
    def _json(self) -> Dict[str, Any]:
        return dict(
            __class__=self.__class__.__name__,
            __kw__={},
            __args__=[self.title, self.entries],
        )

def blog_j_encode(object: Union[Blog_J, Post_J, Any]) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second,
            ),
        )
    else:
        try:
            encoding = object._json
        except AttributeError:
            encoding = json.JSONEncoder().default(object)
        return encoding


travel3 = Blog_J("Travel")
travel3.append(
    Post_J(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel3.append(
    Post_J(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)

test_json_4 = """
    >>> text = json.dumps(travel3, indent=4, default=blog_j_encode)
    >>> print(text)
    {
        "__class__": "Blog_J",
        "__kw__": {},
        "__args__": [
            "Travel",
            [
                {
                    "__class__": "Post_J",
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime",
                            "__args__": [],
                            "__kw__": {
                                "year": 2013,
                                "month": 11,
                                "day": 14,
                                "hour": 17,
                                "minute": 25,
                                "second": 0
                            }
                        },
                        "title": "Hard Aground",
                        "rst_text": "Some embarrassing revelation. Including \u2639 and \u2693",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#ICW"
                        ]
                    },
                    "__args__": []
                },
                {
                    "__class__": "Post_J",
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime",
                            "__args__": [],
                            "__kw__": {
                                "year": 2013,
                                "month": 11,
                                "day": 18,
                                "hour": 15,
                                "minute": 30,
                                "second": 0
                            }
                        },
                        "title": "Anchor Follies",
                        "rst_text": "Some witty epigram.",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#Mistakes"
                        ]
                    },
                    "__args__": []
                }
            ]
        ]
    }
"""

# Example 5: JSON: Super-Flexible Date Encoding
# #############################################

# Right at the edge of the envelope for dates. This may be too much flexibility.
# There's an ISO standard for dates, and using it is simpler.

# For other unique data objects, however, this kind of pattern may be helpful
# for providing a way to parse complex strings.

# Changes to the class definitions
def blog_j2_encode(object: Union[Blog_J, Post_J, Any]) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime.strptime",
            __args__=[object.strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S"],
            __kw__={},
        )
    else:
        try:
            encoding = object._json
        except AttributeError:
            encoding = json.JSONEncoder().default(object)
        return encoding


test_json_5 = """
    >>> text = json.dumps(travel3, indent=4, default=blog_j2_encode)
    >>> print(text)
    {
        "__class__": "Blog_J",
        "__kw__": {},
        "__args__": [
            "Travel",
            [
                {
                    "__class__": "Post_J",
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime.strptime",
                            "__args__": [
                                "2013-11-14T17:25:00",
                                "%Y-%m-%dT%H:%M:%S"
                            ],
                            "__kw__": {}
                        },
                        "title": "Hard Aground",
                        "rst_text": "Some embarrassing revelation. Including \u2639 and \u2693",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#ICW"
                        ]
                    },
                    "__args__": []
                },
                {
                    "__class__": "Post_J",
                    "__kw__": {
                        "date": {
                            "__class__": "datetime.datetime.strptime",
                            "__args__": [
                                "2013-11-18T15:30:00",
                                "%Y-%m-%dT%H:%M:%S"
                            ],
                            "__kw__": {}
                        },
                        "title": "Anchor Follies",
                        "rst_text": "Some witty epigram.",
                        "tags": [
                            "#RedRanger",
                            "#Whitby42",
                            "#Mistakes"
                        ]
                    },
                    "__args__": []
                }
            ]
        ]
    }
    
    >>> from pprint import pprint
    >>> copy = json.loads(text, object_hook=blog_decode)
    >>> print(copy.title)
    Travel
    >>> pprint(copy.entries)
    [Post_J(date=datetime.datetime(2013, 11, 14, 17, 25), title='Hard Aground', rst_text='Some embarrassing revelation. Including ☹ and ⚓', tags=['#RedRanger', '#Whitby42', '#ICW']),
     Post_J(date=datetime.datetime(2013, 11, 18, 15, 30), title='Anchor Follies', rst_text='Some witty epigram.', tags=['#RedRanger', '#Whitby42', '#Mistakes'])]
"""

with (Path.cwd()/"data"/"ch10.json").open("w", encoding="UTF-8") as target:
    json.dump(travel3, target, separators=(",", ":"), default=blog_j2_encode)

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
