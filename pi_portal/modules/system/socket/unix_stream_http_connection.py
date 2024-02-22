"""UnixStreamHTTPConnection class."""

import http.client
import os
import socket
from typing import Optional


class UnixStreamHTTPConnection(http.client.HTTPConnection):
  """HTTP connection over a unix socket.

  :param unix_socket: Path to the unix socket to open.
  """

  blocksize: int

  def __init__(
      self,
      unix_socket: str,
      timeout: Optional[int] = None,
      blocksize: int = 8192,
  ) -> None:
    super().__init__("localhost", timeout=timeout, blocksize=blocksize)
    self.unix_socket = unix_socket

  def connect(self) -> None:
    """Open a unix socket on the specified host."""

    if not os.path.exists(self.unix_socket):
      raise IOError(f"Socket {self.unix_socket} does not exist!")

    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.settimeout(self.timeout)
    self.sock.connect(self.unix_socket)
