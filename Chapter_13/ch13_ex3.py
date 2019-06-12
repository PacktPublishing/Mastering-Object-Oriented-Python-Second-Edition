#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 3.
"""


# Problem Domain
# ==============

from typing import Dict, Any, Tuple, List
from dataclasses import dataclass, asdict
import random
import secrets
from enum import Enum


class Status(str, Enum):
    UPDATED = "Updated"
    CREATED = "Created"


@dataclass
class Dice:
    roll: List[int]
    identifier: str
    status: str

    def reroll(self, keep_positions: List[int]) -> None:
        for i in range(len(self.roll)):
            if i not in keep_positions:
                self.roll[i] = random.randint(1, 6)
        self.status = Status.UPDATED


def make_dice(n_dice: int) -> Dice:
    # Could also be a @classmethod
    return Dice(
        roll=[random.randint(1, 6) for _ in range(n_dice)],
        identifier=secrets.token_urlsafe(8),
        status=Status.CREATED,
    )


# FLASK Restful Web Service
# =========================


from flask import Flask, jsonify, request, url_for, Blueprint, current_app, abort
from typing import Dict, Any, Tuple, List
from http import HTTPStatus

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Chapter 13. Example 3",
        "version": "2019.02",
        "description": "Rolls dice",
    },
    "paths": {
        "/rolls": {
            "post": {
                "description": "first roll",
                "responses": {201: {"description": "Success"}},
            },
            "get": {
                "description": "current state",
                "responses": {200: {"description": "Current state"}},
            },
            "patch": {
                "description": "subsequent roll",
                "responses": {200: {"description": "Modified"}},
            }
        }
    }
}


SESSIONS: Dict[str, Dice] = {}


rolls = Blueprint("rolls", __name__)


@rolls.route("/openapi.json")
def openapi() -> Dict[str, Any]:
    # See dice_openapi.json for full specification
    return jsonify(OPENAPI_SPEC)


@rolls.route("/rolls", methods=["POST"])
def make_roll() -> Tuple[Dict[str, Any], HTTPStatus, Dict[str, str]]:
    body = request.get_json(force=True)
    if set(body.keys()) != {"dice"}:
        raise BadRequest(f"Extra fields in {body!r}")
    try:
        n_dice = int(body["dice"])
    except ValueError as ex:
        raise BadRequest(f"Bad 'dice' value in {body!r}")

    dice = make_dice(n_dice)
    SESSIONS[dice.identifier] = dice
    current_app.logger.info(f"Rolled roll={dice!r}")

    headers = {"Location": url_for("rolls.get_roll", identifier=dice.identifier)}
    return jsonify(asdict(dice)), HTTPStatus.CREATED, headers


@rolls.route("/rolls/<identifier>", methods=["GET"])
def get_roll(identifier) -> Tuple[Dict[str, Any], HTTPStatus]:
    if identifier not in SESSIONS:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(asdict(SESSIONS[identifier])), HTTPStatus.OK


@rolls.route("/rolls/<identifier>", methods=["PATCH"])
def patch_roll(identifier) -> Tuple[Dict[str, Any], HTTPStatus]:
    if identifier not in SESSIONS:
        abort(HTTPStatus.NOT_FOUND)
    body = request.get_json(force=True)
    if set(body.keys()) != {"keep"}:
        raise BadRequest(f"Extra fields in {body!r}")
    try:
        keep_positions = [int(d) for d in body["keep"]]
    except ValueError as ex:
        raise BadRequest(f"Bad 'keep' value in {body!r}")

    dice = SESSIONS[identifier]
    dice.reroll(keep_positions)

    return jsonify(asdict(dice)), HTTPStatus.OK


class BadRequest(Exception):
    pass


def make_app() -> Flask:

    app = Flask(__name__)
    # Only used for HTML-based sessions...
    # app.secret_key = 'lt0oypOUT9Vu7cbyivfv9hdEzWLlEf_w'

    @app.errorhandler(BadRequest)
    def error_message(ex) -> Tuple[Dict[str, Any], HTTPStatus]:
        current_app.logger.error(f"{ex.args}")
        return jsonify(status="Bad Request", message=ex.args), HTTPStatus.BAD_REQUEST

    app.register_blueprint(rolls)

    return app


test_not_found = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response = client.get("/rando_path")
    >>> response.status
    '404 NOT FOUND'
    >>> response.status_code
    404
    >>> response.data[:55]
    b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
"""

test_post_get_patch = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response1 = client.post("/rolls", json={"dice": 5})
    >>> response1.status
    '201 CREATED'
    >>> response1.status_code
    201
    >>> document1 = response1.get_json()
    >>> document1['roll']
    [1, 1, 1, 3, 2]
    >>> document1['status']
    'Created'
    >>> document1['identifier'] in SESSIONS
    True
    >>> response1.headers['Location'].endswith(document1['identifier'])
    True
    >>> response1.headers['Location'].startswith('http://localhost/rolls/')
    True
    
    >>> response2 = client.get(f"/rolls/{document1['identifier']}")
    >>> response2.status
    '200 OK'
    >>> document2 = response2.get_json()
    >>> document2['roll']
    [1, 1, 1, 3, 2]
    >>> document2['status']
    'Created'
    >>> document2['identifier'] == document1['identifier']
    True

    >>> response3 = client.patch(f"/rolls/{document1['identifier']}", json={"keep": [0, 1, 2]})
    >>> response3.status
    '200 OK'
    >>> document3 = response3.get_json()
    >>> document3['roll']
    [1, 1, 1, 6, 6]
    >>> document3['status']
    'Updated'
    >>> document3['identifier'] == document1['identifier']
    True
"""

test_post_bad_get = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response1 = client.post("/rolls", json={"dice": 5})
    >>> response1.status
    '201 CREATED'
    >>> document1 = response1.get_json()
    >>> document1['roll']
    [1, 1, 1, 3, 2]
    >>> document1['status']
    'Created'

    # Definitely NOT the identifier.
    >>> response2 = client.get(f"/rolls/xyzzy_{document1['identifier']}")
    >>> response2.status
    '404 NOT FOUND'
    >>> document2 = response2.data
    >>> document2[:55]
    b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
"""

test_bad_post = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response1 = client.post("/rolls", json={"not_the_document": "you were looking for"})
    >>> response1.status
    '400 BAD REQUEST'
    >>> document1 = response1.get_json()
    >>> document1['status']
    'Bad Request'
    >>> document1['message']
    ["Extra fields in {'not_the_document': 'you were looking for'}"]
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
