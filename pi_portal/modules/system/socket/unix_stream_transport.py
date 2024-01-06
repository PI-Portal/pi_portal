"""UnixStreamTransport class."""

from typing import Dict, Tuple, Union

from pi_portal.modules.python.xmlrpc import patched_client
from .unix_stream_http_connection import UnixStreamHTTPConnection


class UnixStreamTransport(patched_client.Transport):
  """XML-RPC client transport using a unix socket.

  :param socket_path: Path to the unix socket to open.
  """

  def __init__(
      self,
      socket_path: str,
  ) -> None:
    self.socket_path = socket_path
    super().__init__()

  def make_connection(
      self,
      host: Union[Tuple[str, Dict[str, str]], str],
  ) -> UnixStreamHTTPConnection:
    """Connect to the unix socket, ignoring the host parameter.

    :param host: Unused parameter in this context.
    :returns: A http connection over a unix socket.
    """

    return UnixStreamHTTPConnection(self.socket_path)
