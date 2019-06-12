#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 10. Example 6. XML
"""

# Persistence Classes
# ========================================

# A detail class for micro-blog posts
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, DefaultDict, Dict, Any
from collections import defaultdict
import io
from Chapter_10.ch10_ex1 import travel, rst_render


# XML
# ===================

# Example 1: XML output
# ######################

from dataclasses import dataclass, field, asdict
@dataclass
class Post_X:
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]
    underline: str = field(init=False)
    tag_text: str = field(init=False)

    def __post_init__(self) -> None:
        self.underline = "-"*len(self.title)
        self.tag_text = ' '.join(self.tags)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def xml(self) -> str:
        tags = "".join(f"<tag>{t}</tag>" for t in self.tags)
        return f"""\
<entry>
    <title>{self.title}</title>
    <date>{self.date}</date>
    <tags>{tags}</tags>
    <text>{self.rst_text}</text>
</entry>"""


from dataclasses import dataclass, field, asdict

@dataclass
class Blog_X:
    title: str
    entries: List[Post_X] = field(default_factory=list)
    underline: str = field(init=False)

    def __post_init__(self) -> None:
        self.underline = "="*len(self.title)

    def append(self, post: Post_X) -> None:
        self.entries.append(post)

    def by_tag(self) -> DefaultDict[str, List[Dict[str, Any]]]:
        tag_index: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self.entries:
            for tag in post.tags:
                tag_index[tag].append(asdict(post))
        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def xml(self) -> str:
        children = "\n".join(c.xml() for c in self.entries)
        return f"""\
<blog><title>{self.title}</title>
<entries>
{children}
<entries>
</blog>
"""


travel4 = Blog_X("Travel")
travel4.append(
    Post_X(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel4.append(
    Post_X(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)

test_xml_out_1 = """
    >>> print(travel4.xml())  # doctest: +NORMALIZE_WHITESPACE
    <blog><title>Travel</title>
    <entries>
    <entry>
        <title>Hard Aground</title>
        <date>2013-11-14 17:25:00</date>
        <tags><tag>#RedRanger</tag><tag>#Whitby42</tag><tag>#ICW</tag></tags>
        <text>Some embarrassing revelation. Including ☹ and ⚓</text>
    </entry>
    <entry>
        <title>Anchor Follies</title>
        <date>2013-11-18 15:30:00</date>
        <tags><tag>#RedRanger</tag><tag>#Whitby42</tag><tag>#Mistakes</tag></tags>
        <text>Some witty epigram.</text>
    </entry>
    <entries>
    </blog>
"""

# Example 2: element Tree output
# ##############################

import xml.etree.ElementTree as XML
from typing import cast

class Blog_E(Blog_X):

    def xmlelt(self) -> XML.Element:
        blog = XML.Element("blog")
        title = XML.SubElement(blog, "title")
        title.text = self.title
        title.tail = "\n"
        entities = XML.SubElement(blog, "entries")
        entities.extend(cast('Post_E', c).xmlelt() for c in self.entries)
        blog.tail = "\n"
        return blog


class Post_E(Post_X):

    def xmlelt(self) -> XML.Element:
        post = XML.Element("entry")
        title = XML.SubElement(post, "title")
        title.text = self.title
        date = XML.SubElement(post, "date")
        date.text = str(self.date)
        tags = XML.SubElement(post, "tags")
        for t in self.tags:
            tag = XML.SubElement(tags, "tag")
            tag.text = t
        text = XML.SubElement(post, "rst_text")
        text.text = self.rst_text
        post.tail = "\n"
        return post


travel5 = Blog_E("Travel")
travel5.append(
    Post_E(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel5.append(
    Post_E(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including < & > characters.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)

test_xml_out_2 = """
    >>> tree = XML.ElementTree(travel5.xmlelt())
    >>> text = XML.tostring(tree.getroot())
    >>> print(text.decode('utf-8'))  # doctest: +NORMALIZE_WHITESPACE
    <blog><title>Travel</title>
    <entries><entry><title>Hard Aground</title><date>2013-11-14 17:25:00</date><tags><tag>#RedRanger</tag><tag>#Whitby42</tag><tag>#ICW</tag></tags><rst_text>Some embarrassing revelation. Including &#9785; and &#9875;</rst_text></entry>
    <entry><title>Anchor Follies</title><date>2013-11-18 15:30:00</date><tags><tag>#RedRanger</tag><tag>#Whitby42</tag><tag>#Mistakes</tag></tags><rst_text>Some witty epigram. Including &lt; &amp; &gt; characters.</rst_text></entry>
    </entries></blog>

"""

def build_blog(document: XML.ElementTree) -> Blog_X:
    xml_blog = document.getroot()
    blog = Blog_X(xml_blog.findtext("title"))
    for xml_post in xml_blog.findall("entries/entry"):
        optional_tag_iter = (
            t.text for t in xml_post.findall("tags/tag")
        )
        tags = list(
            filter(None, optional_tag_iter)
        )
        post = Post_X(
            date=datetime.datetime.strptime(
                xml_post.findtext("date"), "%Y-%m-%d %H:%M:%S"
            ),
            title=xml_post.findtext("title"),
            tags=tags,
            rst_text=xml_post.findtext("rst_text"),
        )
        blog.append(post)
    return blog

test_xml_in = """
    >>> tree = XML.ElementTree(travel5.xmlelt())
    >>> text = XML.tostring(tree.getroot())

    >>> document = XML.parse(io.StringIO(text.decode("utf-8")))
    >>> blog = build_blog(document)
    >>> rst_render(blog)  # doctest: +NORMALIZE_WHITESPACE
    Travel
    ======
    <BLANKLINE>
    <BLANKLINE>
        Hard Aground
        ------------
    <BLANKLINE>
        Some embarrassing revelation. Including ☹ and ⚓
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

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
