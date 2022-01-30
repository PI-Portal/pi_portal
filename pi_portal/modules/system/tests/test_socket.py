"""Test the unix stream transport for xmlrpc."""

from unittest import TestCase, mock

from pi_portal.modules.system import socket


class TestUnixStreamTransport(TestCase):
  """Test the UnixStreamTransport class."""

  def setUp(self):
    self.mock_path = '/var/run/mock.socket'
    self.transport = socket.UnixStreamTransport(self.mock_path)

  def test_initialize(self):
    self.assertEqual(self.transport.socket_path, self.mock_path)

  @mock.patch(socket.__name__ + ".UnixStreamHTTPConnection")
  def test_make_connection(self, m_http_stream):
    connection = self.transport.make_connection("https://unused/argument")
    self.assertEqual(connection, m_http_stream.return_value)
    m_http_stream.assert_called_once_with(self.mock_path)


class TestUnixStreamHTTPConnection(TestCase):
  """Test the UnixStreamHTTPConnection class."""

  def setUp(self):
    self.mock_path = '/var/run/mock.socket'
    self.connection = socket.UnixStreamHTTPConnection(self.mock_path)

  @mock.patch(socket.__name__ + ".socket.socket")
  def test_connect(self, m_socket):
    self.connection.connect()
    m_socket.assert_called_once_with(
        socket.socket.AF_UNIX, socket.socket.SOCK_STREAM
    )
    m_socket.return_value.connect.assert_called_once_with(self.mock_path)
