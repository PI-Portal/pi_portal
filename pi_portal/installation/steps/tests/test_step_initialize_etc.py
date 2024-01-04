"""Test the StepInitializeEtc class."""
import logging
from io import StringIO
from typing import Iterable, List
from unittest import mock

import pytest
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_etc
from ..bases import system_call_step
from ..step_initialize_etc import StepInitializeEtc


class TestStepInitializeEtc:
  """Test the StepInitializeEtc class."""

  def build_existing_log_arguments(self, etc_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{etc_path}' ...",
            f"test - INFO - Found existing '{etc_path}' ...",
            f"test - INFO - Setting permissions on '{etc_path}' ...",
            f"test - INFO - Executing: 'chown root:root {etc_path}' ...",
            f"test - INFO - Executing: 'chmod 755 {etc_path}' ...",
        ]
    ) + "\n"

  def build_existing_system_calls(self, etc_path: str) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"chown root:root {etc_path}",
            f"chmod 755 {etc_path}",
        ]
    )

  def build_no_existing_log_arguments(self, etc_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{etc_path}' ...",
            f"test - INFO - Executing: 'mkdir -p {etc_path}' ...",
            f"test - INFO - Setting permissions on '{etc_path}' ...",
            f"test - INFO - Executing: 'chown root:root {etc_path}' ...",
            f"test - INFO - Executing: 'chmod 755 {etc_path}' ...",
        ]
    ) + "\n"

  def build_no_existing_system_calls(
      self,
      etc_folder: str,
  ) -> Iterable[CallType]:
    return map(
        mock.call, [
            f"mkdir -p {etc_folder}",
            f"chown root:root {etc_folder}",
            f"chmod 755 {etc_folder}",
        ]
    )

  def test__initialize__attrs(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
  ) -> None:
    assert isinstance(step_initialize_etc_instance.log, logging.Logger)
    assert step_initialize_etc_instance.etc_paths == [
        "/etc/filebeat",
        "/etc/motion",
        "/etc/pki/tls/certs",
    ]

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_etc_instance.etc_paths:
      expected_system_calls += self.build_no_existing_system_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_etc_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing etc paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing etc paths.\n",
        ]
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__failure(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0, 0, 127]

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_initialize_etc_instance.invoke()

    assert mocked_system.mock_calls == list(
        self.build_no_existing_system_calls("/etc/filebeat")
    )
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing etc paths ...\n",
            self.build_no_existing_log_arguments("/etc/filebeat"),
            "test - ERROR - Command: 'chmod 755 /etc/filebeat' failed!\n",
        ]
    )
    assert str(exc.value) == "Command: 'chmod 755 /etc/filebeat' failed!"

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = ""
    expected_system_calls: List[CallType] = []
    for log_file in step_initialize_etc_instance.etc_paths:
      expected_system_calls += self.build_existing_system_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_etc_instance.invoke()

    assert mocked_system.mock_calls == expected_system_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing etc paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing etc paths.\n",
        ]
    )
