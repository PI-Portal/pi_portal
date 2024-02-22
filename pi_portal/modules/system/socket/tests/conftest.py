"""Test fixtures for the socket modules tests."""
# pylint: disable=redefined-outer-name

from io import BytesIO
from unittest import mock

import pytest
from pi_portal.modules.system.socket import (
    unix_stream_http_client,
    unix_stream_http_connection,
    unix_stream_transport,
)


class MockedResponse(BytesIO):
  status: int
  reason: str


@pytest.fixture
def mocked_socket() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_response() -> "MockedResponse":
  return MockedResponse()


@pytest.fixture
def mocked_os_path_exists() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_socket_path() -> str:
  return "/var/run/mock.socket"


@pytest.fixture
def mocked_unix_stream_http_connection() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def unix_stream_http_client_instance(
    mocked_response: MockedResponse,
    mocked_socket_path: str,
    mocked_unix_stream_http_connection: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> unix_stream_http_client.UnixStreamHttpClient:
  mocked_unix_stream_http_connection. \
    return_value.getresponse.return_value = mocked_response
  monkeypatch.setattr(
      unix_stream_http_client.__name__ + ".UnixStreamHTTPConnection",
      mocked_unix_stream_http_connection,
  )
  return unix_stream_http_client.UnixStreamHttpClient(mocked_socket_path)


@pytest.fixture
def unix_stream_http_connection_instance(
    mocked_socket: mock.Mock,
    mocked_os_path_exists: mock.Mock,
    mocked_socket_path: str,
    monkeypatch: pytest.MonkeyPatch,
) -> unix_stream_http_connection.UnixStreamHTTPConnection:
  monkeypatch.setattr(
      unix_stream_http_connection.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  monkeypatch.setattr(
      unix_stream_http_connection.__name__ + ".socket.socket",
      mocked_socket,
  )
  return unix_stream_http_connection.UnixStreamHTTPConnection(
      mocked_socket_path
  )


@pytest.fixture
def unix_stream_transport_instance(
    mocked_socket_path: str
) -> unix_stream_transport.UnixStreamTransport:
  return unix_stream_transport.UnixStreamTransport(mocked_socket_path)
