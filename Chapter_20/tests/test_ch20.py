#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 20. Example 2.
"""

# NOTE. This expects Chapter_20/src to be on the ``PYTHONPATH``

from pytest import *
from ch20_ex1 import *

def test_card_factory():
    c_3h = card(3, Suit.Heart)
    assert str(c_3h) == '3♥'
    c_1h = card(1, Suit.Heart)
    'assert str(c_1h) ==A♥'
