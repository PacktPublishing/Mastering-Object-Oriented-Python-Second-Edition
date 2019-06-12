#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 2.
"""


# Problem Domain
# ==============


from dataclasses import dataclass, asdict, astuple
from typing import List, Dict, Any, Tuple, NamedTuple
import random


@dataclass(frozen=True)
class Domino:
    v_0: int
    v_1: int

    @property
    def double(self):
        return self.v_0 == self.v_1

    def __repr__(self):
        if self.double:
            return f"Double({self.v_0})"
        else:
            return f"Domino({self.v_0}, {self.v_1})"


class Boneyard:
    """
    >>> random.seed(2)
    >>> b = Boneyard(limit=6)
    >>> len(b._dominoes)
    28
    >>> b.deal(tiles=7, hands=2)
    [[Domino(2, 0), Double(5), Domino(5, 2), Domino(5, 0), Double(0), Domino(6, 3), Domino(2, 1)], [Domino(3, 1), Double(4), Domino(5, 1), Domino(5, 4), Domino(6, 2), Domino(4, 2), Domino(5, 3)]]

    """

    def __init__(self, limit=6):
        self._dominoes = [
            Domino(x, y) for x in range(0, limit + 1) for y in range(0, x + 1)
        ]
        random.shuffle(self._dominoes)

    def deal(self, tiles: int = 7, hands: int = 4) -> List[List[Tuple[int, int]]]:
        if tiles * hands > len(self._dominoes):
            raise ValueError(f"Invalid tiles={tiles}, hands={hands}")
        return [self._dominoes[h:h + tiles] for h in range(0, tiles * hands, tiles)]


# FLASK Restful Web Service
# =========================

from typing import Dict, Any, Tuple

from flask import Flask, jsonify, abort
from http import HTTPStatus

# Application Server

app = Flask(__name__)


@app.route("/dominoes/<n>")
def dominoes(n: str) -> Tuple[Dict[str, Any], int]:
    try:
        hand_size = int(n)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)

    if app.env == "development":
        random.seed(2)
    b = Boneyard(limit=6)
    hand_0 = b.deal(hand_size)[0]
    app.logger.info("Send %r", hand_0)

    return jsonify(status="OK", dominoes=[astuple(d) for d in hand_0]), HTTPStatus.OK


@app.route("/hands/<int:h>/dominoes/<int:c>")
def hands(h: int, c: int) -> Tuple[Dict[str, Any], int]:
    if h == 0 or c == 0:
        return jsonify(
            status="Bad Request", error=[f"hands={h!r}, dominoes={c!r} is invalid"]
        ), HTTPStatus.BAD_REQUEST

    if app.env == "development":
        random.seed(2)
    b = Boneyard(limit=6)
    try:
        hand_list = b.deal(c, h)
    except ValueError as ex:
        return jsonify(status="Bad Request", error=ex.args), HTTPStatus.BAD_REQUEST
    app.logger.info("Send %r", hand_list)

    return jsonify(
        status="OK", dominoes=[[astuple(d) for d in hand] for hand in hand_list]
    ), HTTPStatus.OK


OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "description": "Deals simple hands of dominoes",
        "version": "2019.02",
        "title": "Chapter 13. Example 2",
    },
    "paths": {},
}


@app.route("/openapi.json")
def openapi() -> Dict[str, Any]:
    """
    >>> client = app.test_client()
    >>> response = client.get("/openapi.json")
    >>> response.get_json()['openapi']
    '3.0.0'
    >>> response.get_json()['info']['title']
    'Chapter 13. Example 2'
    """
    # See dominoes_openapi.json for full specification
    return jsonify(OPENAPI_SPEC)


test_openapi_spec = """
    >>> random.seed(2)
    >>> client = app.test_client()
    >>> response = client.get("/openapi.json")
    >>> response.get_json()['openapi']
    '3.0.0'
    >>> response.get_json()['info']['title']
    'Chapter 13. Example 2'
    
    >>> response = client.get("/dominoes/5")
    >>> response.status
    '200 OK'
    >>> response.status_code
    200
    >>> response.get_json()
    {'dominoes': [[2, 0], [5, 5], [5, 2], [5, 0], [0, 0]], 'status': 'OK'}
    
    >>> document = response.get_json()
    >>> hand = list(Domino(*d) for d in document['dominoes'])
    >>> hand
    [Domino(2, 0), Double(5), Domino(5, 2), Domino(5, 0), Double(0)]
    
    >>> response = client.get("hands/2/dominoes/7")
    >>> response.status
    '200 OK'
    >>> response.status_code
    200
    >>> document = response.get_json()
    >>> document
    {'dominoes': [[[5, 3], [1, 0], [4, 1], [3, 3], [2, 1], [2, 0], [3, 0]], [[5, 4], [4, 4], [6, 3], [6, 5], [5, 0], [6, 4], [3, 2]]], 'status': 'OK'}

    >>> hands = list(list(Domino(*d) for d in h) for h in document['dominoes'])
    >>> for player, h in enumerate(hands):
    ...     for d in h:
    ...         if d.double:
    ...             print(player, d)
    0 Double(3)
    1 Double(4)
    
    >>> response = client.get("hands/nope/dominoes/7")
    >>> response.status
    '404 NOT FOUND'
    >>> response = client.get("hands/0/dominoes/nope")
    >>> response.status
    '404 NOT FOUND'

    >>> response = client.get("hands/0/dominoes/7")
    >>> response.status
    '400 BAD REQUEST'
    >>> response.get_json()
    {'error': ['hands=0, dominoes=7 is invalid'], 'status': 'Bad Request'}
    >>> response = client.get("hands/4/dominoes/0")
    >>> response.status
    '400 BAD REQUEST'
    >>> response.get_json()
    {'error': ['hands=4, dominoes=0 is invalid'], 'status': 'Bad Request'}

    >>> response = client.get("hands/7/dominoes/7")
    >>> response.status
    '400 BAD REQUEST'
    >>> response.get_json()
    {'error': ['Invalid tiles=7, hands=7'], 'status': 'Bad Request'}
"""


__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
