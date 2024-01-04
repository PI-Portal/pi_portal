"""Test the StepStartSupervisor class."""

import logging
from unittest import mock

from .. import step_start_supervisor
from ..bases import service_step


class TestStepStartSupervisor:
  """Test the StepStartSupervisor class."""

  def test__initialize__attrs(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
  ) -> None:
    assert isinstance(step_start_supervisor_instance.log, logging.Logger)
    assert isinstance(
        step_start_supervisor_instance.service,
        service_step.ServiceDefinition,
    )

  def test__initialize__inheritance(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
  ) -> None:
    assert isinstance(
        step_start_supervisor_instance,
        service_step.ServiceStepBase,
    )

  def test__initialize__service(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
  ) -> None:
    assert step_start_supervisor_instance.service.service_name == "supervisor"
    assert step_start_supervisor_instance.service.system_v_service_name == \
        "supervisor"
    assert step_start_supervisor_instance.service.systemd_unit_name == \
        "supervisor.service"

  def test__invoke__enable_method(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
      mocked_service_step_base_enable: mock.Mock,
  ) -> None:

    step_start_supervisor_instance.invoke()

    mocked_service_step_base_enable.assert_called_once_with()

  def test__invoke__start_method(
      self,
      step_start_supervisor_instance: step_start_supervisor.StepStartSupervisor,
      mocked_service_step_base_start: mock.Mock,
  ) -> None:

    step_start_supervisor_instance.invoke()

    mocked_service_step_base_start.assert_called_once_with()
