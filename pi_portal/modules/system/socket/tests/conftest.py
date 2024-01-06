"""Test fixtures for the socket modules tests."""
# pylint: disable=redefined-outer-name

import pytest
from pi_portal.modules.system.socket import (
    unix_stream_http_connection,
    unix_stream_transport,
)


@pytest.fixture
def mocked_socket_path() -> str:
  return "/var/run/mock.socket"


@pytest.fixture
def unix_stream_http_connection_instance(
    mocked_socket_path: str
) -> unix_stream_http_connection.UnixStreamHTTPConnection:
  return unix_stream_http_connection.UnixStreamHTTPConnection(
      mocked_socket_path
  )


@pytest.fixture
def unix_stream_transport_instance(
    mocked_socket_path: str
) -> unix_stream_transport.UnixStreamTransport:
  return unix_stream_transport.UnixStreamTransport(mocked_socket_path)
