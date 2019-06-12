#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 1. Example 5.
"""

# Definition of some classes with doctest-based unit tests.

from types import SimpleNamespace

class EmptyClass:
    pass

EmptyClass2 = SimpleNamespace

EmptyClass3 = type('EmptyClass3', (object,), {})

__test__ = {
    'EmptyClass': '''
        >>> ec = EmptyClass()
        >>> ec.new_attribute = 42
        >>> ec.new_attribute
        42
        >>> ec.undefined  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        AttributeError: 'EmptyClass' object has no attribute 'undefined'
        ''',
    'EmptyClass2': '''
        >>> ec = EmptyClass2()
        >>> ec.new_attribute = 42
        >>> ec.new_attribute
        42
        >>> ec.undefined  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        AttributeError: 'EmptyClass' object has no attribute 'undefined'
        ''',
    'EmptyClass3': '''
        >>> ec = EmptyClass3()
        >>> ec.new_attribute = 42
        >>> ec.new_attribute
        42
        >>> ec.undefined  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        AttributeError: 'EmptyClass' object has no attribute 'undefined'
        ''',
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
