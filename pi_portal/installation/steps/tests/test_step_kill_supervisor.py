"""Test the StepKillSupervisor class."""

import logging
from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.system import process
from .. import step_kill_supervisor


class TestStepKillSupervisor:
  """Test the StepKillSupervisor class."""

  def test__initialize__attrs(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
  ) -> None:
    assert isinstance(step_kill_supervisor_instance.log, logging.Logger)
    assert isinstance(step_kill_supervisor_instance.process, process.Process)
    assert step_kill_supervisor_instance.pid_file_path == config.PID_FILE_MOTION

  @mock.patch(
      step_kill_supervisor.__name__ + ".os.path.exists",
      mock.Mock(return_value=False),
  )
  def test__invoke__no_pid_file(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
      mocked_process_kill: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    step_kill_supervisor_instance.invoke()

    assert mocked_stream.getvalue() == \
         (
            "test - INFO - Killing the supervisor process ...\n"
            "test - INFO - No supervisor process to kill.\n"
            "test - INFO - Done killing the supervisor process.\n"
        )
    mocked_process_kill.assert_not_called()

  @mock.patch(
      step_kill_supervisor.__name__ + ".os.path.exists",
      mock.Mock(return_value=True),
  )
  def test__invoke__pid_file(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
      mocked_process_kill: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    step_kill_supervisor_instance.invoke()

    assert mocked_stream.getvalue() == \
        (
            "test - INFO - Killing the supervisor process ...\n"
            "test - INFO - Done killing the supervisor process.\n"
        )
    mocked_process_kill.assert_called_once_with()
