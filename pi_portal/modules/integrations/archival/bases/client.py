"""Archival client base class."""

import abc

from pi_portal.modules.configuration import state


class ArchivalException(Exception):
  """Exception for Archival errors."""


class ArchivalClientBase:
  """Archival client base class.

  :param partition_name: The data partition of the archival implementation.
  """

  partition_name: str

  def __init__(self, partition_name: str) -> None:
    self.partition_name = partition_name
    self.current_state = state.State()

  @abc.abstractmethod
  def upload(
      self,
      local_file_name: str,
      archival_file_name: str,
  ) -> None:
    """Upload the specified file to the archival service.

    :param local_file_name: The path of the file to upload.
    :param archival_file_name: The archived file that will be created.
    :raises: :class:`ArchivalException`
    """
