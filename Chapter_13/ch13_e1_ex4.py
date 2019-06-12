#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 4.
"""


# REST basics
# ========================================

# Stateless. Roulette.  Base class definitions.

from typing import Dict, Tuple, Optional, List, Iterable, Any, TYPE_CHECKING, cast

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

    def __init__(self):
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

    def __init__(self, wheel):
        self.table = Table(100)
        self.rounds = 0
        self.wheel = wheel

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        # print(environ, file=sys.stderr)
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
                # TODO: Must undo all bets.
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
            if size != "":
                raw = environ["wsgi.input"].read(int(size))
                raise RESTException(
                    "403 FORBIDDEN", f"Data '{raw!r}' not allowed"
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
def roulette_server_4(count: int = 1):
    from wsgiref.simple_server import make_server
    from wsgiref.validate import validator

    wheel = American()
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


def roulette_client(method="GET", path="/", data=None):
    rest = http.client.HTTPConnection("localhost", 8080)
    if data:
        header = {"Content-type": "application/json; charset=utf-8'"}
        params = json.dumps(data).encode("UTF-8")
        rest.request(method, path, params, header)
    else:
        rest.request(method, path)
    response = rest.getresponse()
    raw = response.read().decode("utf-8")
    if 200 <= response.status < 300:
        document = json.loads(raw)
        return document
    else:
        print(response.status, response.reason)
        print(response.getheaders())
        print(raw)


# REST with authentication
# ========================================

# Authentication class definition with password hashing.
from hashlib import sha256
import os


class Authentication:
    iterations = 1000

    def __init__(self, username: bytes, password: bytes, salt: Optional[bytes]=None) -> None:
        """Works with bytes. Not Unicode strings."""
        self.username = username
        self.salt = salt or os.urandom(24)
        self.hash = self._iter_hash(self.iterations, self.salt, username, password)

    @staticmethod
    def _iter_hash(iterations: int, salt: bytes, username: bytes, password: bytes):
        seed = salt + b":" + username + b":" + password
        for i in range(iterations):
            seed = sha256(seed).digest()
        return seed

    def __eq__(self, other: Any) -> bool:
        other = cast("Authentication", other)
        return self.username == other.username and self.hash == other.hash

    def __hash__(self) -> int:
        return hash(self.hash)

    def __repr__(self) -> str:
        salt_x = "".join("{0:x}".format(b) for b in self.salt)
        hash_x = "".join("{0:x}".format(b) for b in self.hash)
        return f"{self.username} {self.iterations:d}:{salt_x}:{hash_x}"

    def match(self, password: bytes) -> bool:
        test = self._iter_hash(self.iterations, self.salt, self.username, password)
        return self.hash == test  # Constant Time is Best


# Collection of users.
class Users(dict):

    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)
        # Can never be found -- dict key is invalid and isn't the username.
        self[""] = Authentication(b"__dummy__", b"Doesn't Matter")

    def add(self, authentication: Authentication) -> None:
        if authentication.username == "":
            raise KeyError("Invalid Authentication")
        self[authentication.username] = authentication

    def match(self, username: bytes, password: bytes) -> bool:
        if username in self and username != "":
            return self[username].match(password)
        else:
            # Time-wasting comparison
            return self[""].match(b"Something which doesn't match")


# Global Objects
users = Users()
users.add(Authentication(b"Aladdin", b"open sesame"))

test_matching = """
    Spike to show user matching rule.
    
    >>> test_salt = bytes(range(24))
    >>> al = Authentication(b"Aladdin", b"open sesame", test_salt)
    >>> al
    b'Aladdin' 1000:0123456789abcdef1011121314151617:a53bdcd6d16acc8fd33fc982c973147f15f6ce43cff4fb83a5f6b267de1
    
    >>> users = Users()
    >>> users.add(Authentication(b"Aladdin", b"open sesame"))

    >>> users.match("", b"Doesn't Matter")
    False
    >>> users.match(b"__dummy__", b"Doesn't Matter")
    False
"""

# Authentication app
import base64


class Authenticate(WSGI):

    def __init__(self, users, target_app):
        self.users = users
        self.target_app = target_app

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        if "HTTP_AUTHORIZATION" in environ:
            scheme, credentials = environ["HTTP_AUTHORIZATION"].split()
            if scheme == "Basic":
                username, password = base64.b64decode(credentials).split(b":")
                if self.users.match(username, password):
                    environ["Authenticate.username"] = username
                    return self.target_app(environ, start_response)
        status = "401 UNAUTHORIZED"
        headers = [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("WWW-Authenticate", 'Basic realm="roulette@localhost"'),
        ]
        start_response(status, headers)
        return ["Not authorized".encode("utf-8")]


# Some app which requires authentication
class Some_App(WSGI):

    def __call__(
        self, environ: "WSGIEnvironment", start_response: "StartResponse"
    ) -> Iterable[bytes]:
        status = "200 OK"
        headers = [("Content-type", "text/plain; charset=utf-8")]
        start_response(status, headers)
        return ["Welcome".encode("UTF-8")]


# Demo client
import base64


def authenticated_client(
    method: str = "GET",
    path: str = "/",
    data: Optional[str] = None,
    username: str = "",
    password: str = "",
) -> Tuple[int, str, str]:
    rest = http.client.HTTPConnection("localhost", 8080)
    headers = {}
    if username and password:
        enc = base64.b64encode(
            username.encode("ascii") + b":" + password.encode("ascii")
        )
        headers["Authorization"] = f"Basic {enc.decode('ascii')}"
    if data:
        headers["Content-type"] = "application/json; charset=utf-8"
        params = json.dumps(data).encode("utf-8")
        rest.request(method, path, params, headers=headers)
    else:
        rest.request(method, path, headers=headers)
    # print(f"*** CLIENT: {headers}")
    response = rest.getresponse()
    raw = response.read().decode("utf-8")
    if response.status == 401:
        print(response.getheaders())
    return response.status, response.reason, raw


# Server
def auth_server(count: int = 1) -> None:
    from wsgiref.simple_server import make_server
    from wsgiref.validate import validator

    secure_app = Some_App()
    authenticated_app = Authenticate(users, secure_app)
    debug = validator(authenticated_app)
    httpd = make_server("", 8080, debug)
    if count is None:
        httpd.serve_forever()
    else:
        for c in range(count):
            httpd.handle_request()


# Demo
def server_5() -> None:
    import concurrent.futures
    import time

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(auth_server, 3)
        time.sleep(0.1)  # Wait for the server to start
        print(authenticated_client("GET", "/player/"))
        print(
            authenticated_client(
                "GET", "/player/", username="Aladdin", password="open sesame"
            )
        )
        print(
            authenticated_client(
                "GET", "/player/", username="Aladdin", password="not right"
            )
        )


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    server_5()
