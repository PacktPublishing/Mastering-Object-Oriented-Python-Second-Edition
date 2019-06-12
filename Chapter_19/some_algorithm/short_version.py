#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 19. Example 3.
"""

# Short-version Implementation
# -------------------------------------

from .abstraction import AbstractSomeAlgorithm


class Implementation_Short(AbstractSomeAlgorithm):
    """
    The Short Version
    """

    def value(self) -> int:
        return 42
