#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 2.
"""


# REST basics
# ========================================

# Stateless. Roulette.  Base class definitions.

from typing import Optional, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from wsgiref.types import WSGIApplication, WSGIEnvironment, StartResponse

import random
from Chapter_13.ch13_ex1 import (
    Wheel,
    Zero,
    DoubleZero,
    American,
    European,
    Response,
    json_get,
)


import sys
import wsgiref.util
import json


# REST Revised: Callable WSGI Applications
# =========================================


class Wheel2(Wheel):

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        winner = self.spin()
        status = "200 OK"
        headers = [("Content-type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [json.dumps(winner).encode("UTF-8")]


class American2(DoubleZero, Wheel2):
    pass


class European2(Zero, Wheel2):
    pass


test_wheel = """
    >>> am = American2(seed=2)
    >>> def mock_start(status, headers):
    ...     print(status, headers)
    >>> am({}, mock_start)
    200 OK [('Content-type', 'application/json; charset=utf-8')]
    [b'{"4": [35, 1], "Black": [1, 1], "Lo": [1, 1], "Even": [1, 1]}']
"""


# A WSGI wrapper application.
import sys


class Wheel3:

    def __init__(self, seed: Optional[int] = None) -> None:
        self.am = American2(seed)
        self.eu = European2(seed)

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        request = wsgiref.util.shift_path_info(environ)  # 1. Parse.
        print("Wheel3", request, file=sys.stderr)  # 2. Logging.
        if request and request.lower().startswith("eu"):  # 3. Evaluate.
            response = self.eu(environ, start_response)
        else:
            response = self.am(environ, start_response)
        return response  # 4. Respond.


test_wheel3 = """
    >>> wheel = Wheel3(seed=2)
    >>> def mock_start(status, headers):
    ...     print(status, headers)
    >>> wheel({"PATH_INFO": "/am"}, mock_start)
    200 OK [('Content-type', 'application/json; charset=utf-8')]
    [b'{"4": [35, 1], "Black": [1, 1], "Lo": [1, 1], "Even": [1, 1]}']
"""

# Revised Server
def roulette_server_3(count: int = 1) -> None:
    from wsgiref.simple_server import make_server

    httpd = make_server("localhost", 8080, Wheel3(2))
    if count is None:
        httpd.serve_forever()
    else:
        for c in range(count):
            httpd.handle_request()


# Wheel3 Demo
# ---------------

# When run as the main script, start a server and interact with it.
def server_3() -> None:

    import concurrent.futures
    import time

    with concurrent.futures.ProcessPoolExecutor() as executor:
        srvr = executor.submit(roulette_server_3, 2)
        time.sleep(0.1)  # Wait for the server to start
        r1 = json_get("/am")
        r2 = json_get("/eu")
        assert (
            str(r1)
            == "200: {'4': [35, 1], 'Black': [1, 1], 'Lo': [1, 1], 'Even': [1, 1]}"
        )
        assert (
            str(r2)
            == "200: {'4': [35, 1], 'Black': [1, 1], 'Lo': [1, 1], 'Even': [1, 1]}"
        )


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    server_3()
