#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 8. Example 1.
"""

# noisyfloat
# ================================

import sys


def trace(frame, event, arg):
    if frame.f_code.co_name.startswith("__"):
        print(frame.f_code.co_name, frame.f_code.co_filename, event)


# sys.settrace(trace)


class NoisyFloat(float):

    def __add__(self, other: float) -> 'NoisyFloat':
        print(self, "+", other)
        return NoisyFloat(super().__add__(other))

    def __radd__(self, other: float) -> 'NoisyFloat':
        print(self, "r+", other)
        return NoisyFloat(super().__radd__(other))

test_noisy_float = """
    >>> x = NoisyFloat(2)
    >>> y = NoisyFloat(3)
    >>> x + y + 2.5
    2.0 + 3.0
    5.0 + 2.5
    7.5
"""


# Fixed Point
# =================================

import numbers
import math
from typing import Union, Optional, Any

class FixedPoint(numbers.Rational):
    __slots__ = ("value", "scale", "default_format")

    def __init__(self, value: Union['FixedPoint', int, float], scale: int = 100) -> None:
        self.value: int
        self.scale: int
        if isinstance(value, FixedPoint):
            self.value = value.value
            self.scale = value.scale
        elif isinstance(value, int):
            self.value = value
            self.scale = scale
        elif isinstance(value, float):
            self.value = int(scale * value + .5)  # Round half up
            self.scale = scale
        else:
            raise TypeError(f"Can't build FixedPoint from {value!r} of {type(value)}")
        digits = int(math.log10(scale))
        self.default_format = "{{0:.{digits}f}}".format(digits=digits)

    def __str__(self) -> str:
        return self.__format__(self.default_format)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__:s}({self.value:d},scale={self.scale:d})"

    def __format__(self, specification: str) -> str:
        if specification == "":
            specification = self.default_format
        return specification.format(self.value / self.scale)  # no rounding

    def numerator(self) -> int:
        return self.value

    def denominator(self) -> int:
        return self.scale

    def __add__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value + other * self.scale
        else:
            new_scale = max(self.scale, other.scale)
            new_value = self.value * (new_scale // self.scale) + other.value * (
                new_scale // other.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __sub__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value - other * self.scale
        else:
            new_scale = max(self.scale, other.scale)
            new_value = self.value * (new_scale // self.scale) - other.value * (
                new_scale // other.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __mul__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value * other
        else:
            new_scale = self.scale * other.scale
            new_value = self.value * other.value
        return FixedPoint(int(new_value), scale=new_scale)

    def __truediv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = int(self.value / other)
        else:
            new_value = int(self.value / (other.value / other.scale))
        return FixedPoint(new_value, scale=self.scale)

    def __floordiv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = int(self.value // other)
        else:
            new_value = int(self.value // (other.value / other.scale))
        return FixedPoint(new_value, scale=self.scale)

    def __mod__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) % other
        else:
            new_value = self.value % (other.value / other.scale)
        return FixedPoint(new_value, scale=self.scale)

    def __pow__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) ** other
        else:
            new_value = (self.value / self.scale) ** (other.value / other.scale)
        return FixedPoint(int(new_value) * self.scale, scale=self.scale)

    def __abs__(self) -> 'FixedPoint':
        return FixedPoint(abs(self.value), self.scale)

    def __float__(self) -> float:
        return self.value / self.scale

    def __int__(self) -> int:
        return int(self.value / self.scale)

    def __trunc__(self) -> int:
        return int(math.trunc(self.value / self.scale))

    def __ceil__(self) -> int:
        return int(math.ceil(self.value / self.scale))

    def __floor__(self) -> int:
        return int(math.floor(self.value / self.scale))

    # reveal_type(numbers.Rational.__round__)

    def __round__(self, ndigits: Optional[int] = 0) -> Any:
        return FixedPoint(round(self.value / self.scale, ndigits=ndigits), self.scale)

    def __neg__(self) -> 'FixedPoint':
        return FixedPoint(-self.value, self.scale)

    def __pos__(self) -> 'FixedPoint':
        return self

    # Note equality among floats isn't a good idea.
    # Also, should FixedPoint(123, 100) equal FixedPoint(1230, 1000)?
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FixedPoint):
            if self.scale == other.scale:
                return self.value == other.value
            else:
                return self.value * other.scale // self.scale == other.value
        else:
            return abs(self.value / self.scale - float(other)) < .5 / self.scale

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __le__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale <= float(other)

    def __lt__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale < float(other)

    def __ge__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale >= float(other)

    def __gt__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale > float(other)

    def __hash__(self) -> int:
        P = sys.hash_info.modulus
        m, n = self.value, self.scale
        # Remove common factors of P.  (Unnecessary if m and n already coprime.)
        while m % P == n % P == 0:
            m, n = m // P, n // P

        if n % P == 0:
            hash_ = sys.hash_info.inf
        else:
            # Fermat's Little Theorem: pow(n, P-1, P) is 1, so
            # pow(n, P-2, P) gives the inverse of n modulo P.
            hash_ = (abs(m) % P) * pow(n, P - 2, P) % P
        if m < 0:
            hash_ = -hash_
        if hash_ == -1:
            hash_ = -2
        return hash_

    def __radd__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.scale + self.value
        else:
            new_scale = max(self.scale, other.scale)
            new_value = other.value * (new_scale // other.scale) + self.value * (
                new_scale // self.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __rsub__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.scale - self.value
        else:
            new_scale = max(self.scale, other.scale)
            new_value = other.value * (new_scale // other.scale) - self.value * (
                new_scale // self.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __rmul__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.value
        else:
            new_scale = self.scale * other.scale
            new_value = other.value * self.value
        return FixedPoint(int(new_value), scale=new_scale)

    def __rtruediv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = self.scale * int(other / (self.value / self.scale))
        else:
            new_value = int((other.value / other.scale) / self.value)
        return FixedPoint(new_value, scale=self.scale)

    def __rfloordiv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = self.scale * int(other // (self.value / self.scale))
        else:
            new_value = int((other.value / other.scale) // self.value)
        return FixedPoint(new_value, scale=self.scale)

    def __rmod__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = other % (self.value / self.scale)
        else:
            new_value = (other.value / other.scale) % (self.value / self.scale)
        return FixedPoint(new_value, scale=self.scale)

    def __rpow__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = other ** (self.value / self.scale)
        else:
            new_value = (other.value / other.scale) ** self.value / self.scale
        return FixedPoint(int(new_value) * self.scale, scale=self.scale)

    def round_to(self, new_scale: int) -> 'FixedPoint':
        f = new_scale / self.scale
        return FixedPoint(int(self.value * f + .5), scale=new_scale)


# test cases to show that ``FixedPoint`` numbers work properly.
test_fp = """
    >>> f1 = FixedPoint(12.34, 100)
    >>> f2 = FixedPoint(1234, 100)
    >>> print(f1, repr(f1))
    12.34 FixedPoint(1234,scale=100)
    >>> print(f2, repr(f2))
    12.34 FixedPoint(1234,scale=100)
    >>> print(f1 * f2, f1 + f2, f1 - f2, f1 / f2)
    152.2756 24.68 0.00 1.00
    >>> print(f1 + 101, f1 * 2, f1 - 101, f1 / 2, f1 % 1, f1 // 2)
    113.34 24.68 -88.66 6.17 0.34 6.17
    >>> print(101 + f2, 2 * f2, 101 - f1, 25 / f1, 1334 % f1, 25 // f1)
    113.34 24.68 88.66 2.00 1.28 2.00
    >>> print("round", round(f1))
    round 12.00
    >>> print("ceil", math.ceil(f1))
    ceil 13
    >>> print("floor", math.floor(f1))
    floor 12
    >>> print("trunc", math.trunc(f1))
    trunc 12

    >>> print("==", f1 == f2, f1 == 12.34, f1 == 1234 / 100, f1 == FixedPoint(12340, 1000))
    == True True True True
    >>> print(hash(f1), hash(f2), hash(FixedPoint(12340, 1000)))
    1521856386081038020 1521856386081038020 1521856386081038020

    >>> f3 = FixedPoint(200, 100)
    >>> print(f3 * f3 * f3, f3 ** 3, 3 ** f3)
    8.000000 8.00 9.00
    
    >>> price = FixedPoint(1299, 100)
    >>> tax_rate = FixedPoint(725, 1000)
    >>> tax = price * tax_rate
    >>> print(tax, tax.round_to(100))
    9.41775 9.42
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
