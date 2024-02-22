"""UnixStreamHttpClient class."""

import json
from dataclasses import dataclass
from http.client import HTTPResponse
from typing import Any, Dict

from pi_portal.modules.system.socket.unix_stream_http_connection import (
    UnixStreamHTTPConnection,
)


class UnixStreamHttpClientException(Exception):
  """Raised during a communications error."""


@dataclass
class UnixStreamHttpResponse:
  """Typed representation of an HTTP response message."""

  status: int
  json: Dict[str, Any]


class UnixStreamHttpClient:
  """A vanilla Python HTTP client over a unix socket.

  :param socket_path: The path to the unix socket.
  """

  def __init__(self, socket_path: str):
    self.socket_path = socket_path

  def post(
      self,
      path: str,
      body: Dict[str, Any],
  ) -> UnixStreamHttpResponse:
    """Send a post request to the server.

    :param path: The HTTP path to make the request to.
    :param body: A python dictionary representing a JSON payload.
    :returns: The server's response.
    """

    conn = UnixStreamHTTPConnection(self.socket_path)

    conn.request(
        "POST",
        path,
        self._encode_payload(body),
        {'Content-Type': 'application/json'},
        encode_chunked=False,
    )

    return self._response(conn.getresponse())

  def _encode_payload(self, raw_body: Dict[str, Any]) -> str:
    return json.dumps(raw_body)

  def _response(self, http_response: HTTPResponse) -> UnixStreamHttpResponse:
    service_response = UnixStreamHttpResponse(
        status=http_response.status,
        json={},
    )
    try:
      response_json = json.loads(http_response.read().decode("utf-8"))
      service_response.json = response_json
    except json.JSONDecodeError:
      service_response.json = {"detail": http_response.reason}
    finally:
      http_response.close()

    if http_response.status > 399:
      raise UnixStreamHttpClientException(service_response.json)
    return service_response
