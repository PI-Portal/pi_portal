"""Test the StepInitializeDataPaths class."""
import logging
from io import StringIO
from typing import Iterable, List
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_etc
from ..bases import system_call_step
from ..step_initialize_data_paths import StepInitializeDataPaths


class TestStepInitializeDataPaths:
  """Test the StepInitializeDataPaths class."""

  chown_arg = f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER}"

  def build_existing_log_arguments(self, data_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{data_path}' ...",
            f"test - INFO - Found existing '{data_path}' ...",
            f"test - INFO - Setting permissions on '{data_path}' ...",
            (
                f"test - INFO - Executing: 'chown {self.chown_arg} "
                f"{data_path}' ..."
            ),
            f"test - INFO - Executing: 'chmod 750 {data_path}' ...",
        ]
    ) + "\n"

  def build_existing_system_calls(self, data_path: str) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"chown {self.chown_arg} {data_path}",
            f"chmod 750 {data_path}",
        ]
    )

  def build_no_existing_log_arguments(self, data_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{data_path}' ...",
            f"test - INFO - Executing: 'mkdir -p {data_path}' ...",
            f"test - INFO - Setting permissions on '{data_path}' ...",
            (
                f"test - INFO - Executing: 'chown {self.chown_arg} "
                f"{data_path}' ..."
            ),
            f"test - INFO - Executing: 'chmod 750 {data_path}' ...",
        ]
    ) + "\n"

  def build_no_existing_system_calls(
      self,
      data_path: str,
  ) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"mkdir -p {data_path}",
            f"chown {self.chown_arg} {data_path}",
            f"chmod 750 {data_path}",
        ]
    )

  def test__initialize__attrs(
      self, step_initialize_data_paths_instance: StepInitializeDataPaths
  ) -> None:
    assert isinstance(step_initialize_data_paths_instance.log, logging.Logger)
    assert step_initialize_data_paths_instance.data_paths == [
        config.PATH_VIDEO_UPLOAD_QUEUE
    ]

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_data_paths_instance.data_paths:
      expected_system_calls += self.build_no_existing_system_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_data_paths_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
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
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0, 0, 127]
    failed_file = config.PATH_VIDEO_UPLOAD_QUEUE

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_initialize_data_paths_instance.invoke()

    assert mocked_system.mock_calls == list(
        self.build_no_existing_system_calls(failed_file)
    )
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing data paths ...\n",
            self.build_no_existing_log_arguments(failed_file),
            f"test - ERROR - Command: 'chmod 750 {failed_file}' failed!\n",
        ]
    )
    assert str(exc.value) == f"Command: 'chmod 750 {failed_file}' failed!"

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_data_paths_instance: StepInitializeDataPaths,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_data_paths_instance.data_paths:
      expected_system_calls += self.build_existing_system_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_data_paths_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing data paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing data paths.\n",
        ]
    )
