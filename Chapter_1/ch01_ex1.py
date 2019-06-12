#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 1. Example 1.
"""

# Show the basics of timeit.

import timeit

method_time = timeit.timeit(
    "obj.method()",
    """
class SomeClass:
    def method(self):
        pass
obj= SomeClass()
""",
)

function_time = timeit.timeit(
    "f()",
    """
def f():
    pass
""",
)

if __name__ == "__main__":
    print(f"Method   {method_time:.4f}")
    print(f"Function {function_time:.4f}")
