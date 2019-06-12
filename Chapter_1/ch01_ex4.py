#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 1. Example 4.
"""


# Simple function with docstring.

def factorial(n: int) -> int:
    """Compute n! recursively.

    :param n: an integer >= 0
    :returns: n!

    Because of Python's stack limitation, this won't
    compute a value larger than about 1000!.

    >>> factorial(5)
    120
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
