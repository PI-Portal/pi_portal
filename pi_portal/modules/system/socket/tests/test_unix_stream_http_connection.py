"""Test the UnixStreamHTTPConnection class."""

import http.client
import socket
from unittest import mock

import pytest
from pi_portal.modules.system.socket.unix_stream_http_connection import (
    UnixStreamHTTPConnection,
)


class TestUnixStreamHTTPConnection:
  """Test the UnixStreamHTTPConnection class."""

  def test_initialize__attributes(
      self,
      mocked_socket_path: str,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection,
  ) -> None:
    assert unix_stream_http_connection_instance.blocksize == 8192
    assert unix_stream_http_connection_instance.timeout is None
    assert unix_stream_http_connection_instance.unix_socket == (
        mocked_socket_path
    )

  def test_initialize__inheritance(
      self,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection,
  ) -> None:
    assert isinstance(
        unix_stream_http_connection_instance,
        http.client.HTTPConnection,
    )

  def test_connect__socket_does_not_exist__raises_exception(
      self,
      mocked_os_path_exists: mock.Mock,
      mocked_socket_path: str,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection,
  ) -> None:
    mocked_os_path_exists.return_value = False

    with pytest.raises(IOError) as exc:
      unix_stream_http_connection_instance.connect()

    assert str(exc.value) == f"Socket {mocked_socket_path} does not exist!"

  def test_connect__socket_exists__creates_connection_correctly(
      self,
      mocked_os_path_exists: mock.Mock,
      mocked_socket: mock.Mock,
      mocked_socket_path: str,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection,
  ) -> None:
    mocked_os_path_exists.return_value = True

    unix_stream_http_connection_instance.connect()

    mocked_socket.assert_called_once_with(socket.AF_UNIX, socket.SOCK_STREAM)
    mocked_socket.return_value.setsockopt.assert_called_once_with(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1,
    )
    mocked_socket.return_value.settimeout.assert_called_once_with(
        unix_stream_http_connection_instance.timeout
    )
    mocked_socket.return_value.connect.assert_called_once_with(
        mocked_socket_path
    )
