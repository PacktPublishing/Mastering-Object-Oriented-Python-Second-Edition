#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 1. Example 3.
"""

def F(n: int) -> int:
    if n in (0, 1):
        return 1
    else:
        return F(n-1) + F(n-2)

test_F_8 = """
    >>> F(8)
    34
"""

def demo():
    print("Good Use", F(8))
    print("Bad Use", F(355/113))

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
