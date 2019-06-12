#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 19. Example 3.
"""

# Long-version Implementation
# -------------------------------------

from .abstraction import AbstractSomeAlgorithm


class Implementation_Long(AbstractSomeAlgorithm):
    """
    The Long Version
    """

    def value(self) -> int:
        return 2 ** 42
