"""CreatePathsAction class."""

import dataclasses
import os
from typing import List

from pi_portal.modules.system import file_system
from .bases import base_action


@dataclasses.dataclass
class FileSystemPath:
  """Represents a local path on the file system.

  :param folder: A boolean indicating a folder should be created.
  :param path: The local path that should be created path.
  :param permissions: The file permissions to set on the created path.
  :param user: The linux user to set as the owner of the created path.
  :param group: The linux user to set as the group of the created path.
  """

  folder: bool
  path: str
  permissions: str = "755"
  user: str = "root"
  group: str = "root"


class CreatePathsAction(base_action.ActionBase):
  """Create and secure the configured file system paths."""

  file_system_paths: List[FileSystemPath]

  def invoke(self) -> None:
    """Create and secure the configured file system paths."""

    for file_system_path in self.file_system_paths:
      fs = file_system.FileSystem(file_system_path.path)

      self.log.info("Creating '%s' ...", file_system_path.path)

      if os.path.exists(file_system_path.path):
        self.log.info("Found existing '%s' ...", file_system_path.path)
        if os.path.isdir(file_system_path.path) != file_system_path.folder:
          raise OSError(self._wrong_file_system_type(file_system_path))
      else:
        fs.create(directory=file_system_path.folder)

      self.log.info("Setting permissions on '%s' ...", file_system_path.path)
      fs.ownership(file_system_path.user, file_system_path.group)
      fs.permissions(file_system_path.permissions)

  def _wrong_file_system_type(self, file_system_path: FileSystemPath) -> str:
    types = {
        True: "directory",
        False: "file",
    }

    return (
        f"The path {file_system_path.path} exists, "
        f"but it is not a {types[file_system_path.folder]}."
    )
