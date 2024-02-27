"""Interact with entities on the local file system."""

import os
import shutil
import time


class FileSystem:
  """An object on the local file system.

  :param path: A path on the local file system.
  """

  path: str
  poll_interval: float = 0.5

  def __init__(self, path: str) -> None:
    self.path = path

  def create(self, directory: bool = False) -> None:
    """Ensure the path exists as either a directory or file.

    :param directory: A boolean indicating whether the target is a directory.
    """

    if directory:
      os.makedirs(self.path, exist_ok=True)
    else:
      os.close(os.open(self.path, os.O_CREAT))

  def ownership(self, user: str, group: str) -> None:
    """Set the owner and group of the file path in question.

    :param user: The Linux user to set ownership to.
    :param group: The Linux group to set ownership to.
    """

    shutil.chown(self.path, user, group)

  def permissions(self, mode: str) -> None:
    """Set the file system permissions for the file path in question.

    :param mode: A three digit octal permission.
    """

    os.chmod(self.path, int(mode, 8))

  def wait_until_exists(self) -> None:
    """Wait until the specified file path exists."""

    while not os.path.exists(self.path):
      time.sleep(self.poll_interval)
