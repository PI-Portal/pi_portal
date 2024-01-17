"""Test the StepInitializeEtc class."""
import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.modules.python.mock import CallType
from .. import step_initialize_etc
from ..bases import base_step
from ..step_initialize_etc import StepInitializeEtc


class TestStepInitializeEtc:
  """Test the StepInitializeEtc class."""

  def build_existing_log_arguments(self, etc_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{etc_path}' ...",
            f"test - INFO - Found existing '{etc_path}' ...",
            f"test - INFO - Setting permissions on '{etc_path}' ...",
        ]
    ) + "\n"

  def build_existing_system_calls(self, etc_path: str) -> List[CallType]:
    return [
        mock.call(etc_path),
        mock.call().ownership("root", "root"),
        mock.call().permissions("755"),
    ]

  def build_no_existing_log_arguments(self, etc_path: str) -> str:
    return "\n".join(
        [
            f"test - INFO - Creating '{etc_path}' ...",
            f"test - INFO - Setting permissions on '{etc_path}' ...",
        ]
    ) + "\n"

  def build_no_existing_system_calls(
      self,
      etc_path: str,
  ) -> List[CallType]:
    return [
        mock.call(etc_path),
        mock.call().create(directory=True),
        mock.call().ownership("root", "root"),
        mock.call().permissions("755"),
    ]

  def test__initialize__attrs(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
  ) -> None:
    assert isinstance(step_initialize_etc_instance.log, logging.Logger)
    assert step_initialize_etc_instance.etc_paths == [
        "/etc/filebeat",
        "/etc/motion",
        "/etc/pi_portal",
        "/etc/pki/tls/certs",
    ]

  def test__initialize__inheritance(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
  ) -> None:
    assert isinstance(
        step_initialize_etc_instance,
        base_step.StepBase,
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=False),
  )
  def test__invoke__no_existing_log_files__success(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    expected_fs_calls: List[CallType] = []
    for log_file in step_initialize_etc_instance.etc_paths:
      expected_fs_calls += self.build_no_existing_system_calls(log_file)
      expected_log_messages += self.build_no_existing_log_arguments(log_file)

    step_initialize_etc_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
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
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = [OSError]

    with pytest.raises(OSError):
      step_initialize_etc_instance.invoke()

    assert mocked_file_system.mock_calls == \
        self.build_no_existing_system_calls("/etc/filebeat")
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing etc paths ...\n",
            self.build_no_existing_log_arguments("/etc/filebeat"),
        ]
    )

  @mock.patch(
      step_initialize_etc.__name__ + '.os.path.exists',
      mock.Mock(return_value=True),
  )
  def test__invoke__existing_log_files__success(
      self,
      step_initialize_etc_instance: StepInitializeEtc,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = ""
    expected_fs_calls: List[CallType] = []
    for log_file in step_initialize_etc_instance.etc_paths:
      expected_fs_calls += self.build_existing_system_calls(log_file)
      expected_log_messages += self.build_existing_log_arguments(log_file)

    step_initialize_etc_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
    assert mocked_stream.getvalue() == "".join(
        [
            "test - INFO - Initializing etc paths ...\n",
            expected_log_messages,
            "test - INFO - Done initializing etc paths.\n",
        ]
    )
