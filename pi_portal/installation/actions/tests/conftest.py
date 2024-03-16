"""Fixtures for the steps modules base class tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Callable, Dict, List, NamedTuple, Optional, Type
from unittest import mock

import pytest
from pi_portal.installation.services.bases import service_definition
from pi_portal.installation.templates import config_file
from .. import (
    action_create_paths,
    action_manage_service,
    action_remote_files,
    action_render_templates,
)

TypeFilePathCreationScenarioCreator = (
    Callable[
        ["FilePathCreationScenario"],
        "FilePathCreationScenarioMocks",
    ]
)


class FilePathCreationScenario(NamedTuple):
  path_exists: bool
  wrong_path_index: Optional[int] = None


class FilePathCreationScenarioMocks(NamedTuple):
  wrong_path: Optional[str]
  expected_type: Optional[str]


@pytest.fixture
def mocked_config_template() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_security() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_http_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_path_isdir() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_manage_service_methods() -> Dict[str, mock.Mock]:
  return {
      operation.value: mock.Mock()
      for operation in action_manage_service.ServiceOperation
  }


@pytest.fixture
def mocked_service_definition() -> service_definition.ServiceDefinition:
  return service_definition.ServiceDefinition(
      service_name="mock_service",
      system_v_service_name="mock_system_v_service",
      systemd_unit_name="mock_systemd_unit",
  )


@pytest.fixture
def mocked_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_file_path_creation_scenario(
    concrete_action_create_paths_instance: action_create_paths.
    CreatePathsAction, mocked_os_path_isdir: mock.Mock,
    monkeypatch: pytest.MonkeyPatch
) -> "TypeFilePathCreationScenarioCreator":

  def setup(
      scenario: "FilePathCreationScenario"
  ) -> "FilePathCreationScenarioMocks":

    scenario_mocks = FilePathCreationScenarioMocks(
        wrong_path=None,
        expected_type=None,
    )

    isdir_return_values: List[bool] = []
    for index, file_system_path in enumerate(
        concrete_action_create_paths_instance.file_system_paths
    ):
      return_value = file_system_path.folder

      if scenario.wrong_path_index == index:
        scenario_mocks = FilePathCreationScenarioMocks(
            wrong_path=file_system_path.path,
            expected_type="directory" if file_system_path.folder else "file"
        )
        return_value = not file_system_path.folder

      isdir_return_values.append(return_value)

    mocked_os_path_isdir.side_effect = isdir_return_values
    monkeypatch.setattr(
        action_create_paths.__name__ + '.os.path.exists',
        mock.Mock(return_value=scenario.path_exists),
    )

    return scenario_mocks

  return setup


@pytest.fixture
def concrete_action_create_paths_class(
    mocked_file_system: mock.Mock,
    mocked_os_path_isdir: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[action_create_paths.CreatePathsAction]:
  monkeypatch.setattr(
      action_create_paths.__name__ + ".file_system.FileSystem",
      mocked_file_system,
  )
  monkeypatch.setattr(
      action_create_paths.__name__ + ".os.path.isdir",
      mocked_os_path_isdir,
  )

  class ConcreteCreatePathsAction(action_create_paths.CreatePathsAction):
    file_system_paths = [
        action_create_paths.FileSystemPath(
            folder=True,
            path="/path1/folder1",
            user="root",
            permissions="755",
            group="root",
        ),
        action_create_paths.FileSystemPath(
            folder=True,
            path="/path2/folder2",
            user="admin",
            permissions="750",
            group="root",
        ),
        action_create_paths.FileSystemPath(
            folder=False,
            path="/path3/file1",
            user="user",
            permissions="700",
            group="user",
        ),
    ]

  return ConcreteCreatePathsAction


@pytest.fixture
def concrete_action_create_paths_instance(
    concrete_action_create_paths_class: Type[
        action_create_paths.CreatePathsAction],
    installer_logger_stdout: logging.Logger,
) -> action_create_paths.CreatePathsAction:
  return concrete_action_create_paths_class(installer_logger_stdout)


@pytest.fixture
def concrete_action_manage_service_class(
    mocked_service_definition: service_definition.ServiceDefinition,
    mocked_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[action_manage_service.ManageServiceAction]:
  monkeypatch.setattr(
      action_manage_service.base_system_call_action.__name__ + ".os.system",
      mocked_system,
  )

  class ConcreteManageServiceAction(action_manage_service.ManageServiceAction):

    service = mocked_service_definition
    operation = action_manage_service.ServiceOperation.DISABLE

  return ConcreteManageServiceAction


@pytest.fixture
def concrete_action_manage_service_instance(
    concrete_action_manage_service_class: Type[
        action_manage_service.ManageServiceAction],
    installer_logger_stdout: logging.Logger,
) -> action_manage_service.ManageServiceAction:
  return concrete_action_manage_service_class(installer_logger_stdout)


@pytest.fixture
def concrete_action_remote_files_class(
    mocked_file_security: mock.Mock,
    mocked_file_system: mock.Mock,
    mocked_http_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[action_remote_files.RemoteFilesAction]:
  monkeypatch.setattr(
      action_remote_files.__name__ + ".file_security.FileSecurity",
      mocked_file_security,
  )
  monkeypatch.setattr(
      action_remote_files.__name__ + ".file_system.FileSystem",
      mocked_file_system,
  )
  monkeypatch.setattr(
      action_remote_files.__name__ + ".http.HttpClient",
      mocked_http_client,
  )

  class ConcreteRemoteFilesAction(action_remote_files.RemoteFilesAction):

    remote_files = [
        action_remote_files.RemoteFile(
            sha256="expected_sha256_1",
            target="/path/target1.txt",
            url="https://remote.com/source1.txt",
            permissions="750",
            user="test_user1",
        ),
        action_remote_files.RemoteFile(
            sha256="expected_sha256_2",
            target="/path/target2.sh",
            url="https://remote.com/source2.sh",
            permissions="755",
            user="test_user2",
        )
    ]

  return ConcreteRemoteFilesAction


@pytest.fixture
def concrete_action_remote_files_instance(
    concrete_action_remote_files_class: Type[
        action_remote_files.RemoteFilesAction],
    installer_logger_stdout: logging.Logger,
) -> action_remote_files.RemoteFilesAction:

  instance = concrete_action_remote_files_class(installer_logger_stdout)
  # Serially during testing
  instance.fail_fast = False
  instance.worker_count = 1
  return instance


@pytest.fixture
def concrete_action_render_templates_class(
    mocked_file_system: mock.Mock,
    mocked_config_template: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[action_render_templates.RenderTemplatesAction]:
  monkeypatch.setattr(
      config_file.__name__ + ".ConfileFileTemplate",
      mocked_config_template,
  )
  monkeypatch.setattr(
      action_render_templates.__name__ + ".file_system.FileSystem",
      mocked_file_system,
  )

  class ConcreteTemplatesRenderAction(
      action_render_templates.RenderTemplatesAction
  ):
    templates = [
        action_render_templates.FileSystemTemplate(
            source="templates/file1",
            destination="/etc/file1",
            permissions="750",
            user="test_user1",
            group="test_group1",
        ),
        action_render_templates.FileSystemTemplate(
            source="templates/file2",
            destination="/etc/file2",
            permissions="755",
            user="test_user2",
            group="test_group2",
        )
    ]

  return ConcreteTemplatesRenderAction


@pytest.fixture
def concrete_templates_render_action_instance(
    concrete_action_render_templates_class: Type[
        action_render_templates.RenderTemplatesAction],
    installer_logger_stdout: logging.Logger,
) -> action_render_templates.RenderTemplatesAction:
  return concrete_action_render_templates_class(installer_logger_stdout)
