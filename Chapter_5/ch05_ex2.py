#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 5. Example 2.
"""
import numbers
import decimal
import collections.abc

test_membership = """
>>> isinstance(42, numbers.Number) 
True
>>> 355/113             
3.1415929203539825
>>> isinstance(355/113, numbers.Number) 
True

>>> issubclass(decimal.Decimal, numbers.Number)
True
>>> issubclass(decimal.Decimal, numbers.Integral) 
False
>>> issubclass(decimal.Decimal, numbers.Real) 
False
>>> issubclass(decimal.Decimal, numbers.Complex) 
False
>>> issubclass(decimal.Decimal, numbers.Rational) 
False

"""

test_iterator = """
>>> x = [1, 2, 3]
>>> iter(x)  # doctest: +ELLIPSIS
<list_iterator object at ...>
>>> x_iter = iter(x)
>>> next(x_iter)
1
>>> next(x_iter) 
2
>>> next(x_iter) 
3
>>> next(x_iter)  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
  File "/Users/slott/miniconda3/envs/py37/lib/python3.7/doctest.py", line 1329, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__.__test__.test_iterator[6]>", line 1, in <module>
    next(x_iter)
StopIteration
>>> isinstance(x_iter, collections.abc.Iterator) 
True

"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
