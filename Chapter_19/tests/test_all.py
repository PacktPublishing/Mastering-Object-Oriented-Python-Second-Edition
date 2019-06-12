# A Test Module
# ----------------

"""Test all features of some_algorithm.

Requires some_algorithm package be on the PYTHONPATH.
"""

# Imports

import unittest
from Chapter_19 import some_algorithm

# Test Case


class TestSomeAlgorithm(unittest.TestCase):

    def test_import_should_see_value(self):
        x = some_algorithm.SomeAlgorithm()
        assert 2 ** 42 == x.value()


# Run the implicit test suite if this is used as a main program.

if __name__ == "__main__":
    unittest.main(exit=False)
