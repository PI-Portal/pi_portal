"""Provide a unix stream transport for xmlrpc."""

import http.client
import socket
import xmlrpc.client
from typing import Dict, Tuple, Union


class UnixStreamHTTPConnection(http.client.HTTPConnection):
  """An http connection over a unix socket."""

  def connect(self):
    """Open a unix socket to the specified host."""

    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.sock.connect(self.host)


class UnixStreamTransport(xmlrpc.client.Transport):
  """An xmlrpc client Transport using a unix socket."""

  def __init__(self, socket_path: str):
    self.socket_path = socket_path
    super(UnixStreamTransport, self).__init__()  # pylint: disable=super-with-arguments

  def make_connection(self, host: Union[Tuple[str, Dict[str, str]], str]):
    """Connect to the specified unix socket, ignoring the host parameter."""

    return UnixStreamHTTPConnection(self.socket_path)
