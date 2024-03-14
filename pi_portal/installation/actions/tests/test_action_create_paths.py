"""Test the CreatePathsAction class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

from pi_portal.modules.python.mock import CallType
from .. import action_create_paths
from ..action_create_paths import CreatePathsAction, FileSystemPath
from ..bases import base_action


class TestCreatePathsAction:
  """Test the CreatePathsAction class."""

  def build_logging__existing_path(
      self,
      file_system_path: FileSystemPath,
  ) -> str:
    return "\n".join(
        [
            f"INFO - Creating '{file_system_path.path}' ...",
            f"INFO - Found existing '{file_system_path.path}' ...",
            f"INFO - Setting permissions on '{file_system_path.path}' ...",
        ]
    ) + "\n"

  def build_mock_file_system_calls__existing_path(
      self,
      file_system_path: FileSystemPath,
  ) -> List[CallType]:
    return [
        mock.call(file_system_path.path),
        mock.call().ownership(file_system_path.user, file_system_path.group),
        mock.call().permissions(file_system_path.permissions),
    ]

  def build_logging__non_existing_path(
      self,
      file_system_path: FileSystemPath,
  ) -> str:
    return "\n".join(
        [
            f"INFO - Creating '{file_system_path.path}' ...",
            f"INFO - Setting permissions on '{file_system_path.path}' ...",
        ]
    ) + "\n"

  def build_mock_file_system_calls__non_existing_path(
      self,
      file_system_path: FileSystemPath,
  ) -> List[CallType]:
    return [
        mock.call(file_system_path.path),
        mock.call().create(directory=file_system_path.folder),
        mock.call().ownership(file_system_path.user, file_system_path.group),
        mock.call().permissions(file_system_path.permissions),
    ]

  def test_initialize__attributes(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
  ) -> None:
    assert isinstance(concrete_action_create_paths_instance.log, logging.Logger)

  def test_initialize__file_system_path(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
  ) -> None:
    assert len(concrete_action_create_paths_instance.file_system_paths) == 3
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      assert isinstance(
          file_system_path,
          FileSystemPath,
      )

  def test_initialize__inheritance(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
  ) -> None:
    assert isinstance(
        concrete_action_create_paths_instance,
        base_action.ActionBase,
    )

  @mock.patch(
      action_create_paths.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test_invoke__existing__logging(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_log_messages += self.build_logging__existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  @mock.patch(
      action_create_paths.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test_invoke__existing__file_system_calls(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    expected_fs_calls: List[CallType] = []
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_fs_calls += self.build_mock_file_system_calls__existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  @mock.patch(
      action_create_paths.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test_invoke__non_existing__logging(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_log_messages += self.build_logging__non_existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  @mock.patch(
      action_create_paths.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test_invoke__non_existing__file_system_calls(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    expected_fs_calls: List[CallType] = []
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_fs_calls += (
          self.
          build_mock_file_system_calls__non_existing_path(file_system_path)
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
