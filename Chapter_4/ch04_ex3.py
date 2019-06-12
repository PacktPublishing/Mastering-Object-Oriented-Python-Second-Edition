#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 4. Example 3.
"""
from typing import Any, Optional
from dataclasses import dataclass

from Chapter_4.ch04_ex1 import Deck, BlackJackCard

# Eagerly Computed Attributes
# ============================

# Compute early and often. This is rather complex because it
# derives any one from the other two. The ``Optional[float]`` is misleading.


@dataclass
class RateTimeDistance:

    rate: Optional[float] = None
    time: Optional[float] = None
    distance: Optional[float] = None

    def __post_init__(self) -> None:
        if self.rate is not None and self.time is not None:
            self.distance = self.rate * self.time
        elif self.rate is not None and self.distance is not None:
            self.time = self.distance / self.rate
        elif self.time is not None and self.distance is not None:
            self.rate = self.distance / self.time


test_rtd = """
    >>> rtd = RateTimeDistance(rate=6.3, time=8.25, distance=None)
    >>> print(f"Rate={rtd.rate}, Time={rtd.time}, Distance={rtd.distance}")
    Rate=6.3, Time=8.25, Distance=51.975
    
    >>> RateTimeDistance(rate=5.2, time=9.5)
    RateTimeDistance(rate=5.2, time=9.5, distance=49.4)
    >>> RateTimeDistance(distance=48.5, rate=6.1)
    RateTimeDistance(rate=6.1, time=7.950819672131148, distance=48.5)
    
    >>> r1 = RateTimeDistance(time=1, rate=0)
    >>> r1.distance = -99
    >>> r1
    RateTimeDistance(rate=0, time=1, distance=-99)
"""

# Dynamic Attributes
# ==================


class RTD_Dynamic:

    def __init__(self) -> None:
        self.rate: float
        self.time: float
        self.distance: float

        super().__setattr__("rate", None)
        super().__setattr__("time", None)
        super().__setattr__("distance", None)

    def __repr__(self) -> str:
        clauses = []
        if self.rate:
            clauses.append(f"rate={self.rate}")
        if self.time:
            clauses.append(f"time={self.time}")
        if self.distance:
            clauses.append(f"distance={self.distance}")
        return (f"{self.__class__.__name__}" f"({', '.join(clauses)})")

    def __setattr__(self, name: str, value: float) -> None:
        if name == "rate":
            super().__setattr__("rate", value)
        elif name == "time":
            super().__setattr__("time", value)
        elif name == "distance":
            super().__setattr__("distance", value)

        if self.rate and self.time:
            super().__setattr__("distance", self.rate * self.time)
        elif self.rate and self.distance:
            super().__setattr__("time", self.distance / self.rate)
        elif self.time and self.distance:
            super().__setattr__("rate", self.distance / self.time)


test_rtd_dynamic = """
    >>> rtd = RTD_Dynamic()
    >>> rtd.time = 9.5
    >>> rtd
    RTD_Dynamic(time=9.5)
    >>> rtd.rate = 6.25
    >>> rtd
    RTD_Dynamic(rate=6.25, time=9.5, distance=59.375)
    >>> rtd.distance
    59.375
    
    >>> rtd.time = None
    >>> rtd.rate = 6.125
    >>> rtd
    RTD_Dynamic(rate=6.125, time=9.5, distance=58.1875)
    
"""

# Descriptors
# =====================

# A Non-Data descriptor example where the descriptor object
# reads a local cache file to set class-level parameters

from pathlib import Path
from typing import Type


class PersistentState:
    """Abstract superclass to use a StateManager object"""
    _saved: Path


class StateManager:
    """May create a directory. Sets _saved in the instance."""

    def __init__(self, base: Path) -> None:
        self.base = base

    def __get__(self, instance: PersistentState, owner: Type) -> Path:
        if not hasattr(instance, "_saved"):
            class_path = self.base / owner.__name__
            class_path.mkdir(exist_ok=True, parents=True)
            instance._saved = class_path / str(id(instance))
        return instance._saved


class PersistentClass(PersistentState):
    state_path = StateManager(Path.cwd() / "data" / "state")

    def __init__(self, a: int, b: float) -> None:
        self.a = a
        self.b = b
        self.c: Optional[float] = None
        self.state_path.write_text(repr(vars(self)))

    def calculate(self, c: float) -> float:
        self.c = c
        self.state_path.write_text(repr(vars(self)))
        return self.a * self.b + self.c

    def __str__(self) -> str:
        return self.state_path.read_text()


test_persist = """
    >>> x = PersistentClass(1, 2)
    >>> str(x)  # doctest: +ELLIPSIS
    "{'a': 1, 'b': 2, 'c': None, '_saved': ...)}"
    >>> x.calculate(3)
    5
    >>> str(x)  # doctest: +ELLIPSIS
    "{'a': 1, 'b': 2, 'c': 3, '_saved': ...)}"
"""

# A data descriptor example with data in the containing instance.


class Conversion:
    """Depends on a standard value."""
    conversion: float
    standard: str

    def __get__(self, instance: Any, owner: type) -> float:
        return getattr(instance, self.standard) * self.conversion

    def __set__(self, instance: Any, value: float) -> None:
        setattr(instance, self.standard, value / self.conversion)


class Standard(Conversion):
    """Defines a standard value."""
    conversion = 1.0


class Speed(Conversion):
    standard = "standard_speed"  # KPH


class KPH(Standard, Speed):
    pass


class Knots(Speed):
    conversion = 0.5399568


class MPH(Speed):
    conversion = 0.62137119


class Trip:
    kph = KPH()
    knots = Knots()
    mph = MPH()

    def __init__(
        self,
        distance: float,
        kph: Optional[float] = None,
        mph: Optional[float] = None,
        knots: Optional[float] = None,
    ) -> None:
        self.distance = distance  # Nautical Miles
        if kph:
            self.kph = kph
        elif mph:
            self.mph = mph
        elif knots:
            self.knots = knots
        else:
            raise TypeError("Impossible pattern of None values")
        self.time = self.distance / self.knots

    def __str__(self) -> str:
        return (
            f"distance: {self.distance} nm, "
            f"rate: {self.kph} "
            f"kph = {self.mph} "
            f"mph = {self.knots} knots, "
            f"time = {self.time} hrs"
        )


test_trip = """
    >>> m2 = Trip(distance=13.2, knots=5.9)
    >>> print(m2)
    distance: 13.2 nm, rate: 10.92680006993152 kph = 6.789598762345432 mph = 5.9 knots, time = 2.23728813559322 hrs
    >>> print(f"Speed: {m2.mph:.3f} mph")
    Speed: 6.790 mph
    >>> m2.standard_speed
    10.92680006993152
"""

__test__ = {
    name: value for name, value in locals().items() if name.startswith("test_")
}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
