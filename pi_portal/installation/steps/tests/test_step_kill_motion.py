"""Test the StepKillMotion class."""
import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.system import process
from .. import step_kill_motion
from ..bases import system_call_step


class TestStepKillMotion:
  """Test the StepKillMotion class."""

  def test__initialize__attrs(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
  ) -> None:
    assert isinstance(step_kill_motion_instance.log, logging.Logger)
    assert isinstance(step_kill_motion_instance.process, process.Process)
    assert step_kill_motion_instance.pid_file_path == config.PID_FILE_MOTION

  @mock.patch(
      step_kill_motion.__name__ + ".os.path.exists",
      mock.Mock(return_value=False),
  )
  def test__invoke__no_pid_file__system_call_success(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
      mocked_process_kill: mock.Mock,
      mocked_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_system.return_value = 0

    step_kill_motion_instance.invoke()

    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Killing the motion process ...\n"
          "test - INFO - No motion process to kill.\n"
          "test - INFO - Done killing the motion process.\n"
          "test - INFO - Removing motion from startup ...\n"
          "test - INFO - Executing: 'update-rc.d -f motion remove' ...\n"
          "test - INFO - Done removing motion from startup.\n"
        )
    mocked_process_kill.assert_not_called()
    mocked_system.assert_called_once_with("update-rc.d -f motion remove")

  @mock.patch(
      step_kill_motion.__name__ + ".os.path.exists",
      mock.Mock(return_value=True),
  )
  def test__invoke__pid_file__system_call_success(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      mocked_process_kill: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0

    step_kill_motion_instance.invoke()

    assert mocked_stream.getvalue() == \
           (
             "test - INFO - Killing the motion process ...\n"
             "test - INFO - Done killing the motion process.\n"
             "test - INFO - Removing motion from startup ...\n"
             "test - INFO - Executing: 'update-rc.d -f motion remove' ...\n"
             "test - INFO - Done removing motion from startup.\n"
           )
    mocked_process_kill.assert_called_once_with()
    mocked_system.assert_called_once_with("update-rc.d -f motion remove")

  @mock.patch(
      step_kill_motion.__name__ + ".os.path.exists",
      mock.Mock(return_value=True),
  )
  def test__invoke__pid_file__system_call_failure(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
      mocked_process_kill: mock.Mock,
  ) -> None:
    mocked_system.return_value = 12

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_kill_motion_instance.invoke()

    assert mocked_stream.getvalue() == \
           (
             "test - INFO - Killing the motion process ...\n"
             "test - INFO - Done killing the motion process.\n"
             "test - INFO - Removing motion from startup ...\n"
             "test - INFO - Executing: 'update-rc.d -f motion remove' ...\n"
             "test - ERROR - Command: 'update-rc.d -f motion remove' failed!\n"
           )
    mocked_process_kill.assert_called_once_with()
    mocked_system.assert_called_once_with("update-rc.d -f motion remove")
    assert exc.value.args == (
        "Command: 'update-rc.d -f motion remove' failed!",
    )
