"""UnixStreamHTTPConnection class."""

import http.client
import socket


class UnixStreamHTTPConnection(http.client.HTTPConnection):
  """HTTP connection over a unix socket.

  :param host: Path to the unix socket to open.
  """

  def connect(self) -> None:
    """Open a unix socket on the specified host."""

    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.sock.connect(self.host)
