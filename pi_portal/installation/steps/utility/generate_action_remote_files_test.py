"""A generic test suite for RemoteFilesAction subclasses."""

from typing import Type

from pi_portal.installation.actions.action_remote_files import (
    RemoteFile,
    RemoteFilesAction,
)


class GenericRemoteFilesActionTest:
  """A generic test suite for RemoteFilesAction subclasses."""

  action_class: Type[RemoteFilesAction]

  def test_initialize__remote_files(self) -> None:
    for remote_file in self.action_class.remote_files:
      assert isinstance(
          remote_file,
          RemoteFile,
      )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.action_class,
        RemoteFilesAction,
    )
