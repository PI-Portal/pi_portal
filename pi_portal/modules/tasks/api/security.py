"""Security for the task scheduler api server."""

import os
import time

from pi_portal import config
from pi_portal.modules.system.file_system import FileSystem


class SocketSecurity:
  """Secure permissions on the unvicorn unix socket."""

  polling_interval = 0.5
  socket_permissions = "600"
  socket_dir_permissions = "700"

  def __init__(self) -> None:
    self.fs_socket = FileSystem(config.PI_PORTAL_TASK_MANAGER_SOCKET)
    self.fs_socket_dir = FileSystem(
        os.path.dirname(config.PI_PORTAL_TASK_MANAGER_SOCKET)
    )
    self.fs_socket_dir.create(directory=True)
    self.fs_socket_dir.permissions(self.socket_dir_permissions)

  def rewrite_permissions(self) -> None:
    """Wait for the socket to be written to disk, then change permissions."""

    while not os.path.exists(self.fs_socket.path):
      time.sleep(self.polling_interval)

    self.fs_socket.permissions(self.socket_permissions)
    self.fs_socket_dir.permissions(self.socket_dir_permissions)
