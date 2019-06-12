#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 16. Example 7.
"""


# Warnings
# ====================

# Deprecation

import warnings


class Player:
    """version 2.1"""

    def bet(self) -> None:
        warnings.warn(
            "bet is deprecated, use place_bet",
            DeprecationWarning, stacklevel=2)
        pass


warnings.simplefilter("always", category=DeprecationWarning)
p2 = Player()
p2.bet()

# Configuration

import warnings

try:
    import simulation_model_1 as model
except ImportError as e:
    warnings.warn(repr(e))
if 'model' not in globals():
    try:
        import simulation_model_2 as model
    except ImportError as e:
        warnings.warn(repr(e))
if 'model' not in globals():
    # raise ImportError("Missing simulation_model_1 and simulation_model_2")
    pass


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
