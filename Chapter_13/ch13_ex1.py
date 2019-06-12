#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 1.
"""


# REST basics
# ========================================

# Object and state

test_example_1 = """
>>> from dataclasses import dataclass, asdict
>>> import json

>>> @dataclass
... class Greeting:
...     message: str
    
>>> g = Greeting("Hello World")
>>> text = json.dumps(asdict(g))
>>> text
'{"message": "Hello World"}'
>>> text.encode('utf-8')
b'{"message": "Hello World"}'
"""

# Stateless Roulette Server
# ==========================

# Base class definitions.

from typing import (
    Dict,
    Tuple,
    Optional,
    Callable,
    List,
    Union,
    Iterator,
    NamedTuple,
    Any,
    Type,
    Iterable,
    TYPE_CHECKING,
)
from abc import abstractmethod
import random


class Wheel:
    """Abstract, zero bins omitted."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self.rng = random.Random()
        self.rng.seed(seed)
        self.bins = [
            {
                str(n): (35, 1),
                self.redblack(n): (1, 1),
                self.hilo(n): (1, 1),
                self.evenodd(n): (1, 1),
            }
            for n in range(1, 37)
        ]
        self.bins.extend(self.zero())

    @abstractmethod
    def zero(self) -> List[Dict[str, Tuple[int, int]]]:
        pass

    @staticmethod
    def redblack(n: int) -> str:
        return "Red" if n in (
            1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
        ) else "Black"

    @staticmethod
    def hilo(n: int) -> str:
        return "Hi" if n >= 19 else "Lo"

    @staticmethod
    def evenodd(n: int) -> str:
        return "Even" if n % 2 == 0 else "Odd"

    def spin(self) -> Dict[str, Tuple[int, int]]:
        return self.rng.choice(self.bins)


class Zero:

    def zero(self) -> List[Dict[str, Tuple[int, int]]]:
        return [{"0": (35, 1)}]


class DoubleZero(Zero):

    def zero(self) -> List[Dict[str, Tuple[int, int]]]:
        z_bins = super().zero()
        z_bins += [{"00": (35, 1)}]
        return z_bins


class American(DoubleZero, Wheel):
    pass


class European(Zero, Wheel):
    pass


# Some global objects used by a WSGI application function
american = American(9973)
european = European(9973)

test_demonstrate_wheel = """
    >>> american.bins[-2:]
    [{'0': (35, 1)}, {'00': (35, 1)}]
    >>> european.bins[-1]
    {'0': (35, 1)}

    >>> for i in range(7):
    ...     print(american.spin())
    {'25': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}
    {'18': (35, 1), 'Red': (1, 1), 'Lo': (1, 1), 'Even': (1, 1)}
    {'20': (35, 1), 'Black': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'21': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}
    {'32': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'34': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'21': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}

    >>> for i in range(7):
    ...     print(european.spin())
    {'25': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}
    {'18': (35, 1), 'Red': (1, 1), 'Lo': (1, 1), 'Even': (1, 1)}
    {'20': (35, 1), 'Black': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'21': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}
    {'32': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'34': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Even': (1, 1)}
    {'21': (35, 1), 'Red': (1, 1), 'Hi': (1, 1), 'Odd': (1, 1)}
"""

import sys
import wsgiref.util
import json

if TYPE_CHECKING:
    from wsgiref.types import WSGIApplication, WSGIEnvironment, StartResponse


def wsgi_wheel(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    request = wsgiref.util.shift_path_info(environ)  # 1. Parse.
    print("wheel", repr(request), file=sys.stderr)  # 2. Logging.
    if request and request.lower().startswith("eu"):  # 3. Evaluate.
        winner = european.spin()
    else:
        winner = american.spin()
    status = "200 OK"  # 4. Respond.
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [json.dumps(winner).encode("UTF-8")]


# A function we can call to start a server
# which handles a finite number of requests.
# Handy for testing.
from wsgiref.simple_server import make_server


def roulette_server(count: int = 1) -> None:
    httpd = make_server("", 8080, wsgi_wheel)
    if count is None:
        httpd.serve_forever()
    else:
        for c in range(count):
            httpd.handle_request()


# REST Client
# -------------

# A REST client that simply loads a JSON document.
import http.client
import json
from typing import NamedTuple


class Response(NamedTuple):
    status: int
    headers: Dict[str, str]
    content: Optional[Any]

    def __str__(self) -> str:
        return f"{self.status}: {self.content}"


def json_get(path: str = "/") -> Response:
    rest = http.client.HTTPConnection("localhost", 8080, timeout=5)
    rest.request("GET", path)
    response = rest.getresponse()
    # print(f"client: {response.status} {response.reason}")
    # print(f"  {response.getheaders()}")
    raw = response.read().decode("utf-8")
    # print(f"  {raw}")
    try:
        document = json.loads(raw)
    except json.decoder.JSONDecodeError as ex:
        document = None
    return Response(response.status, dict(response.getheaders()), document)


# Roulette Demo
# --------------

# When run as the main script, start a server and interact with it.
# Note that the subprocess will inherit the state of the wheel from the parent
# process; the results are therefore based on the seed, and deterministic.


def server() -> None:
    import concurrent.futures
    import time

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # We'll make four requests. This allows for a very clean termination of a test server.
        srvr = executor.submit(roulette_server, 4)
        time.sleep(0.1)  # Wait for the server to start
        r1 = json_get()
        r2 = json_get()
        r3 = json_get("/european/")
        r4 = json_get("/european/")
        assert (
            str(r1)
            == "200: {'22': [35, 1], 'Black': [1, 1], 'Hi': [1, 1], 'Even': [1, 1]}"
        )
        assert (
            str(r2)
            == "200: {'15': [35, 1], 'Black': [1, 1], 'Lo': [1, 1], 'Odd': [1, 1]}"
        )
        assert (
            str(r3)
            == "200: {'22': [35, 1], 'Black': [1, 1], 'Hi': [1, 1], 'Even': [1, 1]}"
        )
        assert (
            str(r4)
            == "200: {'15': [35, 1], 'Black': [1, 1], 'Lo': [1, 1], 'Odd': [1, 1]}"
        )


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    server()
