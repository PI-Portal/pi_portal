"""Test the CreatePathsAction class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.modules.python.mock import CallType
from ..action_create_paths import CreatePathsAction, FileSystemPath
from ..bases import base_action
from .conftest import (
    FilePathCreationScenario,
    TypeFilePathCreationScenarioCreator,
)


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

  @pytest.mark.parametrize(
      "scenario",
      [FilePathCreationScenario(path_exists=True)],
  )
  def test_invoke__existing__correct_type__logging(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_stream: StringIO,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    setup_file_path_creation_scenario(scenario)
    expected_log_messages = ""
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_log_messages += self.build_logging__existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  @pytest.mark.parametrize(
      "scenario",
      [FilePathCreationScenario(path_exists=True)],
  )
  def test_invoke__existing__correct_type__calls_os_path_isdir(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_os_path_isdir: mock.Mock,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    setup_file_path_creation_scenario(scenario)
    expected_isdir_calls: List[CallType] = []
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_isdir_calls += [mock.call(file_system_path.path)]

    concrete_action_create_paths_instance.invoke()

    assert mocked_os_path_isdir.mock_calls == expected_isdir_calls

  @pytest.mark.parametrize(
      "scenario",
      [FilePathCreationScenario(path_exists=True)],
  )
  def test_invoke__existing__correct_type__file_system_calls(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_file_system: mock.Mock,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    setup_file_path_creation_scenario(scenario)
    expected_fs_calls: List[CallType] = []
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_fs_calls += self.build_mock_file_system_calls__existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  @pytest.mark.parametrize(
      "scenario",
      [
          FilePathCreationScenario(path_exists=True, wrong_path_index=0),
          FilePathCreationScenario(path_exists=True, wrong_path_index=2),
      ],
  )
  def test_invoke__existing__wrong_type_folder__raises_exception(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    scenario_mocks = setup_file_path_creation_scenario(scenario)

    with pytest.raises(OSError) as exc:
      concrete_action_create_paths_instance.invoke()

    assert str(exc.value) == (
        f"The path {scenario_mocks.wrong_path} exists, "
        f"but it is not a {scenario_mocks.expected_type}."
    )

  @pytest.mark.parametrize(
      "scenario",
      [FilePathCreationScenario(path_exists=False)],
  )
  def test_invoke__non_existing__logging(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_stream: StringIO,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    setup_file_path_creation_scenario(scenario)
    expected_log_messages = ""
    for file_system_path in (
        concrete_action_create_paths_instance.file_system_paths
    ):
      expected_log_messages += self.build_logging__non_existing_path(
          file_system_path
      )

    concrete_action_create_paths_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  @pytest.mark.parametrize(
      "scenario",
      [FilePathCreationScenario(path_exists=False)],
  )
  def test_invoke__non_existing__file_system_calls(
      self,
      concrete_action_create_paths_instance: CreatePathsAction,
      mocked_file_system: mock.Mock,
      setup_file_path_creation_scenario: TypeFilePathCreationScenarioCreator,
      scenario: FilePathCreationScenario,
  ) -> None:
    setup_file_path_creation_scenario(scenario)
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
