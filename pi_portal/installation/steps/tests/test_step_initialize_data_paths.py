"""Test the StepInitializeDataPaths class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_etc
from ..bases import base_step
from ..step_initialize_data_paths import StepInitializeDataPaths


class TestStepInitializeDataPaths:
  """Test the StepInitializeDataPaths class."""

  def build_existing_log_arguments(self, data_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{data_path}' ...",
            f"test - INFO - Found existing '{data_path}' ...",
            f"test - INFO - Setting permissions on '{data_path}' ...",
        ]
    ) + "\n"

  def build_existing_fs_calls(self, data_path: str) -> List[CallType]:
    return [
        mock.call(data_path),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("750"),
    ]

  def build_no_existing_log_arguments(self, data_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{data_path}' ...",
            f"test - INFO - Setting permissions on '{data_path}' ...",
        ]
    ) + "\n"

  def build_no_existing_fs_calls(
      self,
      data_path: str,
  ) -> List[CallType]:
    return [
        mock.call(data_path),
        mock.call().create(directory=True),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("750"),
    ]

  def test__initialize__attrs(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
  ) -> None:
    assert isinstance(step_initialize_data_paths_instance.log, logging.Logger)
    # pylint: disable=duplicate-code
    assert step_initialize_data_paths_instance.data_paths == [
        config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
        config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
        config.PATH_CAMERA_CONTENT,
        config.PATH_CAMERA_RUN,
        config.PATH_FILEBEAT_CONTENT,
        config.PATH_TASKS_SERVICE_DATABASES,
    ]

  def test__initialize__inheritance(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
  ) -> None:
    assert isinstance(
        step_initialize_data_paths_instance,
        base_step.StepBase,
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    expected_fs_calls: List[CallType] = []
    for log_file in step_initialize_data_paths_instance.data_paths:
      expected_fs_calls += self.build_no_existing_fs_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_data_paths_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing data paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing data paths.\n",
        ]
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__failure(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = [OSError]
    failed_file = config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD

    with pytest.raises(OSError):
      step_initialize_data_paths_instance.invoke()

    assert mocked_file_system.mock_calls == \
        self.build_no_existing_fs_calls(failed_file)
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing data paths ...\n",
            self.build_no_existing_log_arguments(failed_file),
        ]
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    expected_fs_calls: List[CallType] = []
    for log_file in step_initialize_data_paths_instance.data_paths:
      expected_fs_calls += self.build_existing_fs_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_data_paths_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing data paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing data paths.\n",
        ]
    )
