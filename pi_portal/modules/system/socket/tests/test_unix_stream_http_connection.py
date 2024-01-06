"""Test the UnixStreamHTTPConnection class."""

import socket
from unittest import mock

from pi_portal.modules.system.socket import unix_stream_http_connection
from pi_portal.modules.system.socket.unix_stream_http_connection import (
    UnixStreamHTTPConnection,
)


class TestUnixStreamHTTPConnection:
  """Test the UnixStreamHTTPConnection class."""

  def test_initialize__attributes(
      self, mocked_socket_path: str,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection
  ) -> None:
    assert unix_stream_http_connection_instance.host == mocked_socket_path

  @mock.patch(unix_stream_http_connection.__name__ + ".socket.socket")
  def test_connect(
      self,
      m_socket: mock.Mock,
      mocked_socket_path: str,
      unix_stream_http_connection_instance: UnixStreamHTTPConnection,
  ) -> None:
    unix_stream_http_connection_instance.connect()

    m_socket.assert_called_once_with(socket.AF_UNIX, socket.SOCK_STREAM)
    m_socket.return_value.connect.assert_called_once_with(mocked_socket_path)
