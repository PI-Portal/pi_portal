"""Test the StepInitializeLogging class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_logging
from ..bases import base_step
from ..step_initialize_logging import StepInitializeLogging


class TestStepInitializeLogging:
  """Test the StepInitializeLogging class."""

  def build_existing_base_log_arguments(self) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{config.LOG_FILE_BASE_FOLDER}' ...",
            f"test - INFO - Found existing "
            f"'{config.LOG_FILE_BASE_FOLDER}' ...",
            "test - INFO - Setting permissions on "
            f"'{config.LOG_FILE_BASE_FOLDER}' ...",
        ]
    ) + "\n"

  def build_existing_log_arguments(self, log_file: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{log_file}' ...",
            f"test - INFO - Found existing '{log_file}' ...",
            f"test - INFO - Setting permissions on '{log_file}' ...",
        ]
    ) + "\n"

  def build_existing_base_fs_calls(self) -> List[CallType]:
    return [
        mock.call(config.LOG_FILE_BASE_FOLDER),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("750"),
    ]

  def build_existing_fs_calls(self, log_file: str) -> List[CallType]:
    return [
        mock.call(log_file),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("600"),
    ]

  def build_no_existing_base_log_arguments(self) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{config.LOG_FILE_BASE_FOLDER}' ...",
            "test - INFO - Setting permissions on "
            f"'{config.LOG_FILE_BASE_FOLDER}' ...",
        ]
    ) + "\n"

  def build_no_existing_log_arguments(self, log_file: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{log_file}' ...",
            f"test - INFO - Setting permissions on '{log_file}' ...",
        ]
    ) + "\n"

  def build_no_existing_base_fs_calls(self) -> List[CallType]:
    return [
        mock.call(config.LOG_FILE_BASE_FOLDER),
        mock.call().create(directory=True),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("750"),
    ]

  def build_no_existing_system_calls(self, log_file: str) -> List[CallType]:
    return [
        mock.call(log_file),
        mock.call().create(),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("600"),
    ]

  def test__initialize__attrs(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
  ) -> None:
    assert isinstance(step_initialize_logging_instance.log, logging.Logger)
    assert step_initialize_logging_instance.log_files == [
        config.LOG_FILE_CONTACT_SWITCH_MONITOR,  # pylint: disable=duplicate-code
        config.LOG_FILE_MOTION,
        config.LOG_FILE_SLACK_BOT,
        config.LOG_FILE_SLACK_CLIENT,
        config.LOG_FILE_TASK_SCHEDULER,
        config.LOG_FILE_TEMPERATURE_MONITOR,
    ]

  def test__initialize__inheritance(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
  ) -> None:
    assert isinstance(
        step_initialize_logging_instance,
        base_step.StepBase,
    )

  @mock.patch(
      step_initialize_logging.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = self.build_no_existing_base_log_arguments()
    expected_fs_calls = self.build_no_existing_base_fs_calls()
    for log_file in step_initialize_logging_instance.log_files:
      expected_fs_calls += self.build_no_existing_system_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_logging_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing logging ...\n",
            expected_log_messages,
            "test - INFO - Done initializing logging.\n",
        ]
    )

  @mock.patch(
      step_initialize_logging.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__failure(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = [None, OSError]
    expected_fs_calls = self.build_no_existing_base_fs_calls()
    expected_fs_calls += self.build_no_existing_system_calls(
        step_initialize_logging_instance.log_files[0]
    )

    with pytest.raises(OSError):
      step_initialize_logging_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing logging ...\n",
            self.build_no_existing_base_log_arguments(),
            self.build_no_existing_log_arguments(
                step_initialize_logging_instance.log_files[0]
            ),
        ]
    )

  @mock.patch(
      step_initialize_logging.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = self.build_existing_base_log_arguments()
    expected_fs_calls = self.build_existing_base_fs_calls()
    for log_file in step_initialize_logging_instance.log_files:
      expected_fs_calls += self.build_existing_fs_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_logging_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing logging ...\n",
            expected_log_messages,
            "test - INFO - Done initializing logging.\n",
        ]
    )
