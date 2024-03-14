"""A generic test suite for CreatePathsAction subclasses."""

from typing import Type

from pi_portal.installation.actions.action_create_paths import (
    CreatePathsAction,
    FileSystemPath,
)


class GenericCreatePathsActionTest:
  """A generic test suite for CreatePathsAction subclasses."""

  action_class: Type[CreatePathsAction]

  def test_initialize__file_system_paths(self) -> None:
    for file_system_folder in self.action_class.file_system_paths:
      assert isinstance(
          file_system_folder,
          FileSystemPath,
      )

  def test_initialize__inheritance(self) -> None:
    assert issubclass(
        self.action_class,
        CreatePathsAction,
    )
