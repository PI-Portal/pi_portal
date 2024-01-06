"""Test the UnixStreamTransport class."""

from unittest import mock

from pi_portal.modules.system.socket import unix_stream_transport
from pi_portal.modules.system.socket.unix_stream_transport import (
    UnixStreamTransport,
)


class TestUnixStreamTransport:
  """Test the UnixStreamTransport class."""

  def test_initialize__attributes(
      self, mocked_socket_path: str,
      unix_stream_transport_instance: UnixStreamTransport
  ) -> None:
    assert unix_stream_transport_instance.socket_path == mocked_socket_path

  @mock.patch(unix_stream_transport.__name__ + ".UnixStreamHTTPConnection")
  def test_make_connection__creates_http_stream(
      self,
      m_http_stream: mock.Mock,
      mocked_socket_path: str,
      unix_stream_transport_instance: UnixStreamTransport,
  ) -> None:
    connection = unix_stream_transport_instance.make_connection(
        "https://unused/argument"
    )

    assert connection == m_http_stream.return_value
    m_http_stream.assert_called_once_with(mocked_socket_path)
