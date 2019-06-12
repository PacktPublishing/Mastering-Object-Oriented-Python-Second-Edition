#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 19. Example 3.
"""

# Package with variant implementations
# -------------------------------------

# A complex import

import sys

from typing import Type

from Chapter_19.some_algorithm.abstraction import AbstractSomeAlgorithm

SomeAlgorithm: Type[AbstractSomeAlgorithm]

if sys.platform.endswith("32"):
    # print(f"{sys.platform}: SHORT")
    from Chapter_19.some_algorithm.short_version import *

    SomeAlgorithm = Implementation_Short
else:
    # print(f"{sys.platform}: LONG")
    from Chapter_19.some_algorithm.long_version import *

    SomeAlgorithm = Implementation_Long

# Some additional debugging to display the import behavior

print(f"{__name__}: {SomeAlgorithm.__module__}\n{SomeAlgorithm.__doc__}")
