"""Unix stream transport for XMLRPC."""

import http.client
import socket
from typing import Dict, Tuple, Union

from pi_portal.modules.python.xmlrpc import patched_client


class UnixStreamHTTPConnection(http.client.HTTPConnection):
  """An http connection over a unix socket."""

  def connect(self) -> None:
    """Open a unix socket on the specified host."""

    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.sock.connect(self.host)


class UnixStreamTransport(patched_client.Transport):
  """An XMLRPC client transport using a unix socket.

  :param socket_path: Path to the unix socket to open.
  """

  def __init__(self, socket_path: str) -> None:
    self.socket_path = socket_path
    super(UnixStreamTransport, self).__init__()  # pylint: disable=super-with-arguments

  def make_connection(
      self, host: Union[Tuple[str, Dict[str, str]], str]
  ) -> UnixStreamHTTPConnection:
    """Connect to the specified unix socket, ignoring the host parameter.

    :param host: Unused parameter in this context.
    :returns: A http connection over a unix socket.
    """

    return UnixStreamHTTPConnection(self.socket_path)
