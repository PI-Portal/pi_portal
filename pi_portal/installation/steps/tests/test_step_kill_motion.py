"""Test the StepKillMotion class."""
import logging
from unittest import mock

from .. import step_kill_motion
from ..bases import service_step


class TestStepKillMotion:
  """Test the StepKillMotion class."""

  def test__initialize__attrs(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
  ) -> None:
    assert isinstance(step_kill_motion_instance.log, logging.Logger)
    assert isinstance(
        step_kill_motion_instance.service,
        service_step.ServiceDefinition,
    )

  def test__initialize__inheritance(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
  ) -> None:
    assert isinstance(
        step_kill_motion_instance,
        service_step.ServiceStepBase,
    )

  def test__initialize__service(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
  ) -> None:
    assert step_kill_motion_instance.service.service_name == "motion"
    assert step_kill_motion_instance.service.system_v_service_name == \
        "motion"
    assert step_kill_motion_instance.service.systemd_unit_name == \
        "motion.service"

  def test__invoke__disable_method(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
      mocked_service_step_base_disable: mock.Mock,
  ) -> None:

    step_kill_motion_instance.invoke()

    mocked_service_step_base_disable.assert_called_once_with()

  def test__invoke__stop_method(
      self,
      step_kill_motion_instance: step_kill_motion.StepKillMotion,
      mocked_service_step_base_stop: mock.Mock,
  ) -> None:

    step_kill_motion_instance.invoke()

    mocked_service_step_base_stop.assert_called_once_with()
