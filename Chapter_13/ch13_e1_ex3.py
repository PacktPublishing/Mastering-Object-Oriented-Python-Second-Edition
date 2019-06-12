#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 3.
"""


# REST basics
# ========================================

# Stateless. Roulette.  Base class definitions.

from typing import Dict, Tuple, List, Any, Optional, Iterable, TYPE_CHECKING

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


# A WSGI wrapper application.
import sys


class Wheel3:

    def __init__(self) -> None:
        self.am = American2()
        self.eu = European2()

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


# REST with sessions and state
# ========================================

# Player and Bet for Roulette.

# CRUD design issues.
# Player:
# - GET to see stake and rounds played.
# Bet:
# - POST to create a series of bets or decline to bet.
# - GET to see bets.
# Wheel:
# - GET to get spin and payout.

# Stateful object
from collections import defaultdict


class Table:

    def __init__(self, stake: int = 100) -> None:
        self.bets: Dict[str, int] = defaultdict(int)
        self.stake = stake

    def place_bet(self, name: str, amount: int) -> None:
        self.bets[name] += amount

    def clear_bets(self, name: str) -> None:
        self.bets: Dict[str, int] = defaultdict(int)

    def resolve(self, spin: Dict[str, Tuple[int, int]]) -> List[Tuple[str, int, str]]:
        """spin is a dict with bet:(x:y)."""
        details = []
        while self.bets:
            bet, amount = self.bets.popitem()
            if bet in spin:
                x, y = spin[bet]
                self.stake += int(amount * x / y)
                details.append((bet, amount, "win"))
            else:
                self.stake -= amount
                details.append((bet, amount, "lose"))
        return details


# WSGI Applications
class WSGI:

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        raise NotImplementedError


class RESTException(Exception):
    pass


class Roulette(WSGI):

    def __init__(self, wheel: Wheel) -> None:
        self.table = Table(100)
        self.rounds = 0
        self.wheel = wheel

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        # print( environ, file=sys.stderr )
        app = wsgiref.util.shift_path_info(environ)
        try:
            if app and app.lower() == "player":
                return self.player_app(environ, start_response)
            elif app and app.lower() == "bet":
                return self.bet_app(environ, start_response)
            elif app and app.lower() == "wheel":
                return self.wheel_app(environ, start_response)
            else:
                raise RESTException(
                    "404 NOT_FOUND",
                    "Unknown app in {SCRIPT_NAME}/{PATH_INFO}".format_map(environ),
                )
        except RESTException as e:
            status = e.args[0]
            headers = [("Content-type", "text/plain; charset=utf-8")]
            start_response(status, headers, sys.exc_info())
            return [repr(e.args).encode("UTF-8")]

    def player_app(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if environ["REQUEST_METHOD"] == "GET":
            details = dict(stake=self.table.stake, rounds=self.rounds)
            status = "200 OK"
            headers = [("Content-type", "application/json; charset=utf-8")]
            start_response(status, headers)
            return [json.dumps(details).encode("UTF-8")]
        else:
            raise RESTException(
                "405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ),
            )

    def bet_app(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if environ["REQUEST_METHOD"] == "GET":
            details = dict(self.table.bets)
        elif environ["REQUEST_METHOD"] == "POST":
            size = int(environ["CONTENT_LENGTH"])
            raw = environ["wsgi.input"].read(size).decode("UTF-8")
            try:
                data = json.loads(raw)
                if isinstance(data, dict):
                    data = [data]
                for detail in data:
                    self.table.place_bet(detail["bet"], int(detail["amount"]))
            except Exception as e:
                # Must undo all bets.
                raise RESTException(f"403 FORBIDDEN", "Bet {raw!r}")
            details = dict(self.table.bets)
        else:
            raise RESTException(
                "405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ),
            )
        status = "200 OK"
        headers = [("Content-type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [json.dumps(details).encode("UTF-8")]

    def wheel_app(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if environ["REQUEST_METHOD"] == "POST":
            size = environ["CONTENT_LENGTH"]
            if size != "0":
                raw = environ["wsgi.input"].read(int(size))
                raise RESTException(
                    "403 FORBIDDEN", f"Data {raw!r} not allowed"
                )
            spin = self.wheel.spin()
            payout = self.table.resolve(spin)
            self.rounds += 1
            details = dict(
                spin=spin, payout=payout, stake=self.table.stake, rounds=self.rounds
            )
            status = "200 OK"
            headers = [("Content-type", "application/json; charset=utf-8")]
            start_response(status, headers)
            return [json.dumps(details).encode("UTF-8")]
        else:
            raise RESTException(
                "405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ),
            )


test_table = """
    Spike to show that the essential features work.
    
    >>> wheel = American(seed=2)
    >>> roulette = Roulette(wheel)
    >>> data = {"bet": "Black", "amount": 2}
    >>> roulette.table.place_bet(data["bet"], int(data["amount"]))
    >>> print(roulette.table.bets)
    defaultdict(<class 'int'>, {'Black': 2})
    >>> spin = wheel.spin()
    >>> payout = roulette.table.resolve(spin)
    >>> print(spin, payout)
    {'4': (35, 1), 'Black': (1, 1), 'Lo': (1, 1), 'Even': (1, 1)} [('Black', 2, 'win')]
"""

# Server
def roulette_server_3(count: int = 1) -> None:
    from wsgiref.simple_server import make_server
    from wsgiref.validate import validator

    wheel = American(seed=1)
    roulette = Roulette(wheel)
    debug = validator(roulette)
    httpd = make_server("", 8080, debug)
    if count is None:
        httpd.serve_forever()
    else:
        for c in range(count):
            httpd.handle_request()


# Client
import http.client
import json


def roulette_client(
    method: str = "GET",
    path: str = "/",
    data: Optional[Dict[str, str]] = None
) -> Response:
    rest = http.client.HTTPConnection("localhost", 8080)
    if data:
        header = {"Content-type": "application/json; charset=utf-8'"}
        params = json.dumps(data).encode("UTF-8")
        rest.request(method, path, params, header)
    else:
        rest.request(method, path)
    response = rest.getresponse()
    raw = response.read().decode("utf-8")
    try:
        document = json.loads(raw)
    except json.decoder.JSONDecodeError as ex:
        document = raw
    return Response(response.status, dict(response.getheaders()), document)


def server_3() -> None:
    import concurrent.futures
    import time

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(roulette_server_3, 4)
        time.sleep(0.1)  # Wait for the server to start
        r1 = roulette_client("GET", "/player/")
        print(r1)
        r2 = roulette_client("POST", "/bet/", {"bet": "Black", "amount": "2"})
        print(r2)
        r3 = roulette_client("GET", "/bet/")
        print(r3)
        r4 = roulette_client("POST", "/wheel/")
        print(r4)
        assert r1.status == 200 and r1.content == {"stake": 100, "rounds": 0}
        assert r2.status == 200 and r2.content == {"Black": 2}
        assert r3.status == 200 and r3.content == {"Black": 2}
        assert (
            r4.status == 200
            and r4.content == {'spin': {'9': [35, 1], 'Red': [1, 1], 'Lo': [1, 1], 'Odd': [1, 1]}, 'payout': [['Black', 2, 'lose']], 'stake': 98, 'rounds': 1}
        ), f"{r4!r}"


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    server_3()
