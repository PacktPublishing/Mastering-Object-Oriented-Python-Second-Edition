#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 7. Example 4.
"""

# Comparisons
# ======================================

# Using a list vs. a set

import timeit

def performance() -> None:
    list_time = timeit.timeit("l.remove(10); l.append(10)", "l = list(range(20))")
    set_time = timeit.timeit("l.remove(10); l.add(10)", "l = set(range(20))")
    print(f"append; remove: list {list_time:.3f}, set {set_time:.3f}")

    # Using two parallel lists vs. a mapping

    list_2_time = timeit.timeit(
        "i= k.index(10); v[i]= 0", "k=list(range(20)); v=list(range(20))"
    )
    dict_time = timeit.timeit("m[10]= 0", "m=dict(zip(list(range(20)),list(range(20))))")
    print(f"setitem: two lists {list_2_time:.3f}, one dict {dict_time:.3f}")

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)

    performance()
