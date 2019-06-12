#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 7. Example 3.
"""
from typing import List, cast, Any, Optional, Iterable, overload, Union, Iterator

# Extending Classes
# ##############################

# Basic Stats formulae
import math


# New Sequence from Scratch.
# ======================================

# A Binary Search Tree.
#
# http://en.wikipedia.org/wiki/Binary_search_tree
#
import collections.abc
import weakref
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any


class Comparable(metaclass=ABCMeta):

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...


# In case we need a type variable that maps to Comparable
NodeItem = TypeVar("NodeItem", bound=Comparable)


class TreeNode:
    """
    Ideally, there's weakref to the tree;
    tree has the key() function.
    """

    def __init__(
        self,
        item: Optional[Comparable],
        less: Optional["TreeNode"] = None,
        more: Optional["TreeNode"] = None,
        parent: Optional["TreeNode"] = None,
    ) -> None:
        self.item = item
        self.less = less
        self.more = more
        if parent:
            # Can't create a weakref to a None value. Only set if there's a value
            self.parent = parent

    @property
    def parent(self) -> Optional["TreeNode"]:
        return self.parent_ref()

    @parent.setter
    def parent(self, value: "TreeNode") -> None:
        self.parent_ref = weakref.ref(value)

    def __repr__(self) -> str:
        return f"TreeNode({self.item!r}, {self.less!r}, {self.more!r})"

    def find(self, item: Comparable) -> "TreeNode":
        if self.item is None:  # Root
            if self.more:
                return self.more.find(item)
        elif self.item == item:
            return self
        elif self.item > item and self.less:
            return self.less.find(item)
        elif self.item < item and self.more:
            return self.more.find(item)
        raise KeyError

    def __iter__(self) -> Iterator[Comparable]:
        if self.less:
            yield from self.less
        if self.item:
            yield self.item
        if self.more:
            yield from self.more

    def add(self, item: Comparable) -> None:
        if self.item is None:  # Root Special Case
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)
        elif self.item >= item:
            if self.less:
                self.less.add(item)
            else:
                self.less = TreeNode(item, parent=self)
        elif self.item < item:
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)

    def remove(self, item: Comparable) -> None:
        # Recursive search for node
        if self.item is None or item > self.item:
            if self.more:
                self.more.remove(item)
            else:
                raise KeyError
        elif item < self.item:
            if self.less:
                self.less.remove(item)
            else:
                raise KeyError
        else:  # self.item == item
            if self.less and self.more:  # Two children are present
                successor = self.more._least()
                self.item = successor.item
                if successor.item:
                    successor.remove(successor.item)
            elif self.less:  # One child on less
                self._replace(self.less)
            elif self.more:  # One child on more
                self._replace(self.more)
            else:  # Zero children
                self._replace(None)

    def _least(self) -> "TreeNode":
        if self.less is None:
            return self
        return self.less._least()

    def _replace(self, new: Optional["TreeNode"] = None) -> None:
        if self.parent:
            if self == self.parent.less:
                self.parent.less = new
            else:
                self.parent.more = new
        if new is not None:
            new.parent = self.parent


class Tree(collections.abc.MutableSet):

    def __init__(self, source: Iterable[Comparable] = None) -> None:
        self.root = TreeNode(None)
        self.size = 0
        if source:
            for item in source:
                self.root.add(item)
                self.size += 1

    def add(self, item: Comparable) -> None:
        self.root.add(item)
        self.size += 1

    def discard(self, item: Comparable) -> None:
        if self.root.more:
            try:
                self.root.more.remove(item)
                self.size -= 1
            except KeyError:
                pass
        else:
            pass

    def __contains__(self, item: Any) -> bool:
        if self.root.more:
            self.root.more.find(cast(Comparable, item))
            return True
        else:
            return False

    def __iter__(self) -> Iterator[Comparable]:
        if self.root.more:
            for item in iter(self.root.more):
                yield item
        # Otherwise, the tree is empty.

    def __len__(self) -> int:
        return self.size


test_tree = """
    >>> bt = Tree()
    >>> bt.add("Number 1")
    >>> print(list(iter(bt)))
    ['Number 1']
    >>> bt.add("Number 3")
    >>> print(list(iter(bt)))
    ['Number 1', 'Number 3']
    >>> bt.add("Number 2")
    >>> print(list(iter(bt)))
    ['Number 1', 'Number 2', 'Number 3']
    
    >>> print(repr(bt.root))
    TreeNode(None, None, TreeNode('Number 1', None, TreeNode('Number 3', TreeNode('Number 2', None, None), None)))
    >>> print("Number 2" in bt)
    True
    >>> print(len(bt))
    3
    >>> bt.remove("Number 3")
    >>> print(list(iter(bt)))
    ['Number 1', 'Number 2']
    >>> bt.discard("Number 3")  # Should be silent
    >>> bt.remove("Number 3")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.__test__.test_tree[13]>", line 1, in <module>
        bt.remove("Number 3")  # doctest: +IGNORE_EXCEPTION_DETAIL
      File "/Users/slott/miniconda3/envs/py37/lib/python3.7/_collections_abc.py", line 583, in remove
        raise KeyError(value)
    KeyError: 'Number 3'

    >>> bt.add("Number 1")
    >>> print(list(iter(bt)))
    ['Number 1', 'Number 1', 'Number 2']
"""

test_tree_256_randomized_insert_delete = """
    >>> import random

    >>> for i in range(256):
    ...     values = [random.random() for _ in range(i)]
    ...     random.shuffle(values)
    ...     bt = Tree()
    ...     for i in values:
    ...         bt.add(i)
    ...     assert list(bt) == list(sorted(values)), f"IN: {values}, OUT: {list(bt)}"
    ...     random.shuffle(values)
    ...     for i in values:
    ...         bt.remove(i)
    ...         values.remove(i)
    ...         assert list(bt) == list(sorted(values)), f"IN: {values}, OUT: {list(bt)}"
"""

test_tree_merge = """
    >>> s1 = Tree(["Item 1", "Another", "Middle"])
    >>> s2 = Tree(["Another", "More", "Yet More"])
    >>> print(list(s1))
    ['Another', 'Item 1', 'Middle']
    >>> print(list(s2))
    ['Another', 'More', 'Yet More']
    >>> print(list(iter(s1 | s2)))
    ['Another', 'Another', 'Item 1', 'Middle', 'More', 'Yet More']
    >>> union = s1 | s2
    >>> list(union)
    ['Another', 'Another', 'Item 1', 'Middle', 'More', 'Yet More']
    >>> len(union)
    6
    >>> union.remove('Another')
    >>> list(union)
    ['Another', 'Item 1', 'Middle', 'More', 'Yet More']
    
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)


    # performance()
