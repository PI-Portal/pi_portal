"""Test the StepKillSupervisor class."""

import logging
from unittest import mock

from .. import step_kill_supervisor
from ..bases import service_step


class TestStepKillSupervisor:
  """Test the StepKillSupervisor class."""

  def test__initialize__attrs(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
  ) -> None:
    assert isinstance(step_kill_supervisor_instance.log, logging.Logger)
    assert isinstance(
        step_kill_supervisor_instance.service,
        service_step.ServiceDefinition,
    )

  def test__initialize__inheritance(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
  ) -> None:
    assert isinstance(
        step_kill_supervisor_instance,
        service_step.ServiceStepBase,
    )

  def test__initialize__service(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
  ) -> None:
    assert step_kill_supervisor_instance.service.service_name == "supervisor"
    assert step_kill_supervisor_instance.service.system_v_service_name == \
        "supervisor"
    assert step_kill_supervisor_instance.service.systemd_unit_name == \
        "supervisor.service"

  def test__invoke__stop_method(
      self,
      step_kill_supervisor_instance: step_kill_supervisor.StepKillSupervisor,
      mocked_service_step_base_stop: mock.Mock,
  ) -> None:

    step_kill_supervisor_instance.invoke()

    mocked_service_step_base_stop.assert_called_once_with()
