#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 19. Example 1.
"""

import unittest

# Import the test suite.
from Chapter_19.tests import test_all

if __name__ == "__main__":
    # Execute all tests which can be discovered in the suite.
    unittest.main(test_all, verbosity=2)
