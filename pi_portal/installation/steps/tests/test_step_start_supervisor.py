"""Test the StepStartSupervisor class."""

import logging
from io import StringIO
from unittest import mock

import pytest
from .. import step_start_supervisor
from ..bases import system_call_step


class TestStepStartSupervisor:
  """Test the StepStartSupervisor class."""

  def test__initialize__attrs(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
  ) -> None:
    assert isinstance(step_start_supervisor_instance.log, logging.Logger)

  def test__invoke__success(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0

    step_start_supervisor_instance.invoke()

    assert mocked_stream.getvalue() == \
           (
              "test - INFO - Starting the supervisor process ...\n"
              "test - INFO - Executing: 'service supervisor start' ...\n"
              "test - INFO - Done starting the supervisor process.\n"
           )
    mocked_system.assert_called_once_with("service supervisor start")

  def test__invoke__failure(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 127

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_start_supervisor_instance.invoke()

    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Starting the supervisor process ...\n"
          "test - INFO - Executing: 'service supervisor start' ...\n"
          "test - ERROR - Command: 'service supervisor start' failed!\n"
        )
    mocked_system.assert_called_once_with("service supervisor start")
    assert str(exc.value) == "Command: 'service supervisor start' failed!"
