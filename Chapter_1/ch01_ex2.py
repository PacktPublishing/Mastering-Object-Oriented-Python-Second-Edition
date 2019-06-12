#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 1. Example 2.
"""

# pylint: disable=invalid-name
test_list = """
    >>> f = [1, 1, 2, 3]
    >>> f += [f[-1] + f[-2]]
    >>> f
    [1, 1, 2, 3, 5]
    
    >>> f.__getitem__(-1)
    5
    >>> f.__getitem__(-1).__add__(f.__getitem__(-2))
    8
    >>> f.__iadd__([8])
    [1, 1, 2, 3, 5, 8]
    >>> f
    [1, 1, 2, 3, 5, 8]
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
