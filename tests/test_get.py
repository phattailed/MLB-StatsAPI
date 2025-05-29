import sys
import types

# Provide minimal stubs when optional dependencies are missing.  This
# allows importing ``statsapi`` in environments without ``requests`` or
# ``responses`` installed.
try:  # pragma: no cover - used only when requests isn't installed
    import requests  # type: ignore
except Exception:  # pragma: no cover - fallback for offline tests
    requests = types.SimpleNamespace()

    class HTTPError(Exception):
        pass

    requests.get = lambda *a, **k: None
    requests.exceptions = types.SimpleNamespace(HTTPError=HTTPError)
    sys.modules["requests"] = requests
    sys.modules["requests.exceptions"] = requests.exceptions

try:  # pragma: no cover - used only when responses isn't installed
    import responses  # type: ignore
except Exception:  # pragma: no cover - fallback for offline tests
    responses = types.SimpleNamespace()
    responses.GET = "GET"

    def activate(fn=None):
        return fn if fn is not None else (lambda f: f)

    responses.activate = activate
    responses.add = lambda *a, **k: None
    sys.modules["responses"] = responses

import statsapi
import pytest
import requests.exceptions
from unittest.mock import MagicMock


def fake_dict():
    return {
        "foo": {
            "url": "http://www.foo.com",
            "path_params": {
                "ver": {
                    "type": "str",
                    "default": "v1",
                    "leading_slash": False,
                    "trailing_slash": False,
                    "required": True,
                }
            },
            "query_params": ["bar"],
            "required_params": [[]],
        }
    }


def test_get_returns_dictionary(monkeypatch):
    # mock the ENDPOINTS dictionary
    monkeypatch.setattr(statsapi, "ENDPOINTS", fake_dict())
    # mock the requests object
    mock_req = MagicMock()
    monkeypatch.setattr(statsapi, "requests", mock_req)
    # mock the status code to always be 200
    mock_req.get.return_value.status_code = 200

    result = statsapi.get("foo", {"bar": "baz"})
    # assert that result is the same as the return value from calling the json method of a response object
    assert result == mock_req.get.return_value.json.return_value


def test_get_calls_correct_url(monkeypatch):
    # mock the ENDPOINTS dictionary
    monkeypatch.setattr(statsapi, "ENDPOINTS", fake_dict())
    # mock the requests object
    mock_req = MagicMock()
    monkeypatch.setattr(statsapi, "requests", mock_req)

    statsapi.get("foo", {"bar": "baz"})
    mock_req.get.assert_called_with("http://www.foo.com?bar=baz")


def test_get_server_error(monkeypatch):
    # mock the ENDPOINTS dictionary
    monkeypatch.setattr(statsapi, "ENDPOINTS", fake_dict())
    # mock the requests object to simulate a server error
    mock_req = MagicMock()
    monkeypatch.setattr(statsapi, "requests", mock_req)
    mock_resp = mock_req.get.return_value
    mock_resp.status_code = 500
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError()

    with pytest.raises(requests.exceptions.HTTPError):
        statsapi.get("foo", {"bar": "baz"})


def test_get_invalid_endpoint(monkeypatch):
    # mock the ENDPOINTS dictionary
    monkeypatch.setattr(statsapi, "ENDPOINTS", fake_dict())
    # mock the requests object
    mock_req = MagicMock()
    monkeypatch.setattr(statsapi, "requests", mock_req)
    # invalid endpoint
    with pytest.raises(ValueError):
        statsapi.get("bar", {"foo": "baz"})

    # TODO: add test for path requirement not met
    # TODO: add test for required params
