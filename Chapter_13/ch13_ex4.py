#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 13. Example 4.

..  note::

    This example can't easily be tested by the automated test scripts.
    It requires a server to be started.
"""
import requests


def demo(headers=None):
    headers = headers or {}

    get_openapi = requests.get("http://127.0.0.1:5000/openapi.json")
    if get_openapi.status_code == 200:
        document = get_openapi.json()
        if not document['openapi'].startswith('3.0'):
            raise Exception("Not a valid OpenAPI Version")
        if document['info']['version'] != '2019.02':
            raise Exception("Not a useful release")

    roll = requests.post("http://127.0.0.1:5000/roll", json={"dice": 5}, headers=headers)
    print(roll.status_code, roll.reason, roll.headers)
    body = roll.json()
    print(body)

    identifier = body["identifier"]
    roll_url = roll.headers["Location"]

    response = requests.get(f"http://127.0.0.1:5000/roll/{identifier}", headers=headers)
    print(response.status_code, response.reason)
    print(response.json())

    response2 = requests.get(roll_url, headers=headers)
    print(response2.status_code, response2.reason)
    print(response2.json())

    reroll = requests.patch(roll_url, json={"keep": [0, 1]}, headers=headers)
    print(reroll.status_code, reroll.reason)
    print(reroll.json())


import pytest
from unittest.mock import Mock, call


@pytest.fixture
def mock_requests(monkeypatch):
    r0 = requests.Response()
    r0.status_code = 200
    r0._content = b'{"openapi": "3.0.0", "info": {"version": "2019.02"}}'
    r1 = requests.Response()
    r1.status_code = 200
    r1._content = b'{"valid": "json"}'
    r2 = requests.Response()
    r2.status_code = 201
    r2.headers = {"Location": "http://mocked/roll/mockity-mock-mock"}
    r2._content = b'{"status": "OK", "roll": [1, 2, 3, 4, 5, 6], "identifier": "mockity-mock-mock"}'

    mock_module = Mock(
        get=Mock(side_effect=[r0, r1, r1]),
        post=Mock(return_value=r2),
        patch=Mock(return_value=r1),
    )
    monkeypatch.setitem(globals(), "requests", mock_module)
    return mock_module


def test_demo(mock_requests):
    demo()
    assert (
        mock_requests.mock_calls
        == [
            call.get("http://127.0.0.1:5000/openapi.json"),
            call.post("http://127.0.0.1:5000/roll", json={"dice": 5}, headers={}),
            call.get("http://127.0.0.1:5000/roll/mockity-mock-mock", headers={}),
            call.get("http://mocked/roll/mockity-mock-mock", headers={}),
            call.patch("http://mocked/roll/mockity-mock-mock", json={"keep": [0, 1]}, headers={}),
        ]
    )


if __name__ == "__main__":
    pytest.main([__file__])
    demo()
    # demo({"Api-Key": "some_key"})
    # demo({"Api-Key": "nope"})