"""Test the StepInitializeLogging class."""
import logging
from io import StringIO
from typing import Iterable, List
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_logging
from ..bases import system_call_step
from ..step_initialize_logging import StepInitializeLogging


class TestStepInitializeLogging:
  """Test the StepInitializeLogging class."""

  def build_existing_log_arguments(self, log_file: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{log_file}' ...",
            f"test - INFO - Found existing '{log_file}' ...",
            f"test - INFO - Setting permissions on '{log_file}' ...",
            "test - INFO - Executing: 'chown "
            f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} {log_file}' ...",
            f"test - INFO - Executing: 'chmod 600 {log_file}' ...",
        ]
    ) + "\n"

  def build_existing_system_calls(self, log_file: str) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} {log_file}",
            f"chmod 600 {log_file}",
        ]
    )

  def build_no_existing_log_arguments(self, log_file: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{log_file}' ...",
            f"test - INFO - Executing: 'touch {log_file}' ...",
            f"test - INFO - Setting permissions on '{log_file}' ...",
            "test - INFO - Executing: 'chown "
            f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} {log_file}' ...",
            f"test - INFO - Executing: 'chmod 600 {log_file}' ...",
        ]
    ) + "\n"

  def build_no_existing_system_calls(self, log_file: str) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"touch {log_file}",
            f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} {log_file}",
            f"chmod 600 {log_file}",
        ]
    )

  def test__initialize__attrs(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
  ) -> None:
    assert isinstance(step_initialize_logging_instance.log, logging.Logger)
    assert step_initialize_logging_instance.log_files == [
        config.LOG_FILE_CRON_SCHEDULER,  # pylint: disable=duplicate-code
        config.LOG_FILE_DOOR_MONITOR,
        config.LOG_FILE_MOTION,
        config.LOG_FILE_SLACK_BOT,
        config.LOG_FILE_SLACK_CLIENT,
        config.LOG_FILE_TEMPERATURE_MONITOR,
    ]

  @mock.patch(
      step_initialize_logging.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_logging_instance.log_files:
      expected_system_calls += self.build_no_existing_system_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_logging_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
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
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0, 0, 127]

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_initialize_logging_instance.invoke()

    assert mocked_system.mock_calls == list(
        self.build_no_existing_system_calls("/var/log/pi_portal.cron.log")
    )
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing logging ...\n",
            self.build_no_existing_log_arguments("/var/log/pi_portal.cron.log"),
            "test - ERROR - Command: 'chmod 600 "
            "/var/log/pi_portal.cron.log' failed!\n",
        ]
    )
    assert str(
        exc.value
    ) == "Command: 'chmod 600 /var/log/pi_portal.cron.log' failed!"

  @mock.patch(
      step_initialize_logging.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_logging_instance: StepInitializeLogging,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_logging_instance.log_files:
      expected_system_calls += self.build_existing_system_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_logging_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing logging ...\n",
            expected_log_messages,
            "test - INFO - Done initializing logging.\n",
        ]
    )
