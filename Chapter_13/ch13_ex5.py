#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 5.
"""


# FLASK Restful Web Service with State & Open SSL Cert
# ====================================================

# Creating a certificate for common name will be 127.0.0.1 (since we're running locally)
#
# $ openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
# Generating a RSA private key
# ......................................+++++
# ....................+++++
# writing new private key to 'key.pem'
# -----
# You are about to be asked to enter information that will be incorporated
# into your certificate request.
# What you are about to enter is what is called a Distinguished Name or a DN.
# There are quite a few fields but you can leave some blank
# For some fields there will be a default value,
# If you enter '.', the field will be left blank.
# -----
# Country Name (2 letter code) [AU]:US
# State or Province Name (full name) [Some-State]:VA
# Locality Name (eg, city) []:McLean
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:Mastering OO Python 2e
# Organizational Unit Name (eg, section) []:
# Common Name (e.g. server FQDN or YOUR name) []:127.0.0.1
# Email Address []:

# Using the certificate
#
# $ FLASK_APP=ch13_ex5.py FLASK_ENV=development python -m flask run --cert certificate.pem --key key.pem
#
# Your browser will have questions about the authority, since this is self-signed.

from flask import Flask, jsonify, request, url_for, Blueprint, current_app, json, abort
from http import HTTPStatus
from typing import Dict, Any, Tuple, Callable, Set
from pathlib import Path
import secrets
import random

from functools import wraps
from typing import Callable, Set

VALID_API_KEYS: Set[str] = set()


def init_app(app):
    global VALID_API_KEYS
    if app.env == "development":
        VALID_API_KEYS = {"read-only", "admin", "write"}
    else:
        app.logger.info("Loading from {app.config['VALID_KEYS']}")
        raw_lines = (Path(app.config["VALID_KEYS"]).read_text().splitlines())
        VALID_API_KEYS = set(filter(None, raw_lines))


def valid_api_key(view_function: Callable) -> Callable:

    @wraps(view_function)
    def confirming_view_function(*args, **kw):
        api_key = request.headers.get("Api-Key")
        if api_key not in VALID_API_KEYS:
            current_app.logger.error(f"Rejecting Api-Key:{api_key!r}")
            abort(HTTPStatus.UNAUTHORIZED)
        return view_function(*args, **kw)

    return confirming_view_function


def api_key_in(valid_values: Set[str]):

    def concrete_decorator(view_function: Callable) -> Callable:

        @wraps(view_function)
        def confirming_view_function(*args, **kw):
            api_key = request.headers.get("Api-Key")
            if api_key not in valid_values:
                current_app.logger.error(f"Rejecting Api-Key:{api_key!r}")
                abort(HTTPStatus.UNAUTHORIZED)
            return view_function(*args, **kw)

        return confirming_view_function

    return concrete_decorator


SESSIONS: Dict[str, Any] = {}

roll = Blueprint("roll", __name__)


@roll.route("/openapi.json")
def openapi() -> Dict[str, Any]:
    source_path = next(Path.cwd().glob("**/dice_openapi.json"))
    return jsonify(json.loads(source_path.read_text()))


@roll.route("/roll", methods=["POST"])
@valid_api_key
def create_roll() -> Tuple[Any, HTTPStatus, Dict[str, Any]]:
    body = request.get_json(force=True)
    if set(body.keys()) != {"dice"}:
        raise BadRequest(f"Extra fields in {body!r}")
    try:
        n_dice = int(body["dice"])
    except ValueError as ex:
        raise BadRequest(f"Bad 'dice' value in {body!r}")

    roll = [random.randint(1, 6) for _ in range(n_dice)]
    identifier = secrets.token_urlsafe(8)
    SESSIONS[identifier] = roll
    current_app.logger.info(f"Rolled roll={roll!r}, id={identifier!r}")

    headers = {"Location": url_for("roll.get_roll", identifier=identifier)}
    return jsonify(
        roll=roll, identifier=identifier, status="Created"
    ), HTTPStatus.CREATED, headers


@roll.route("/roll/<identifier>", methods=["GET"])
@valid_api_key
def get_roll(identifier) -> Tuple[Dict[str, Any], HTTPStatus]:
    if identifier not in SESSIONS:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(
        roll=SESSIONS[identifier], identifier=identifier, status="OK"
    ), HTTPStatus.OK


@roll.route("/roll/<identifier>", methods=["PATCH"])
@valid_api_key
def patch_roll(identifier) -> Tuple[Dict[str, Any], HTTPStatus]:
    if identifier not in SESSIONS:
        raise BadRequest(f"Unknown {identifier!r}")
    body = request.get_json(force=True)
    if set(body.keys()) != {"keep"}:
        raise BadRequest(f"Extra fields in {body!r}")
    try:
        keep_positions = [int(d) for d in body["keep"]]
    except ValueError as ex:
        raise BadRequest(f"Bad 'keep' value in {body!r}")

    roll = SESSIONS[identifier]
    for i in range(len(roll)):
        if i not in keep_positions:
            roll[i] = random.randint(1, 6)
    SESSIONS[identifier] = roll

    return jsonify(
        roll=SESSIONS[identifier], identifier=identifier, status="OK"
    ), HTTPStatus.OK


class BadRequest(Exception):
    pass


def make_app() -> Flask:
    app = Flask(__name__)
    app.config["VALID_KEYS"] = "valid_keys_file.txt"
    app.config["ENV"] = "development"

    @app.errorhandler(BadRequest)
    def error_message(ex) -> Tuple[Dict[str, Any], HTTPStatus]:
        current_app.logger.error(f"{ex.args}")
        return jsonify(status="Bad Request", message=ex.args), HTTPStatus.BAD_REQUEST

    init_app(app)
    app.register_blueprint(roll)

    return app


test_get_openapi_spec = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response = client.get("/openapi.json")
    >>> response.status
    '200 OK'
    >>> response.status_code
    200
    >>> spec = response.get_json()
    >>> spec['info']['version']
    '2019.02'
    >>> spec['info']['title']
    'Chapter 13. Examples 3 and 5'
"""

test_get_bad_post_roll = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response = client.post("/roll")
    >>> response.status
    '401 UNAUTHORIZED'
"""

test_get_good_post_roll = """
    >>> random.seed(2)
    >>> app = make_app()
    >>> client = app.test_client()
    >>> response = client.post("/roll", json={"dice": 5}, headers=[("Api-Key", "admin")])
    >>> response.status
    '201 CREATED'
    >>> document = response.get_json()
    >>> document['roll']
    [1, 1, 1, 3, 2]
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
