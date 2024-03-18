"""Test the SupervisorProcessProcessor class."""

import logging
from io import StringIO

import pytest
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcessException,
)
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.supervisor_process import ProcessorClass
from .conftest import (
    ProcessManagementScenario,
    TypeProcessManagementScenarioCreator,
)


class TestSupervisorProcessProcessor:
  """Test the SupervisorProcessProcessor class."""

  log_message_prefix = (
      "DEBUG - {task.id} - {task.type} - Processing: '{task}' ...\n"
  )
  log_message_supervisor_management = (
      "INFO - {task.id} - {task.type} - "
      "Supervisord process management request: "
      "'{task.args.process.value}' -> '{task.args.requested_state.value}' ...\n"
  )
  log_message_supervisor_management_failed = (
      "INFO - {task.id} - {task.type} - "
      "Supervisord process already in requested state: "
      "'{task.args.process.value}' -> '{task.args.requested_state.value}' !\n"
  )
  log_message_suffix = (
      "DEBUG - {task.id} - {task.type} - Completed: '{task}'!\n"
      "DEBUG - {task.id} - {task.type} - Task Timing: '{task}'.\n"
  )

  def test_initialize__attributes(
      self,
      supervisor_process_instance: ProcessorClass,
  ) -> None:
    assert supervisor_process_instance.type == \
        TaskType.SUPERVISOR_PROCESS

  def test_initialize__logger(
      self,
      supervisor_process_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        supervisor_process_instance.log,
        logging.Logger,
    )
    assert supervisor_process_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      supervisor_process_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        supervisor_process_instance,
        processor_base.TaskProcessorBase,
    )

  @pytest.mark.parametrize(
      "scenario", [
          ProcessManagementScenario(
              process=ProcessList.CAMERA,
              requested_state=ProcessStatus.STOPPED,
              process_exception=None,
              method_name="stop"
          ),
          ProcessManagementScenario(
              process=ProcessList.CONTACT_SWITCH_MONITOR,
              requested_state=ProcessStatus.RUNNING,
              process_exception=None,
              method_name="start"
          )
      ]
  )
  def test_process__vary_process__vary_state__successful__logging(
      self,
      supervisor_process_instance: ProcessorClass,
      mocked_stream: StringIO,
      setup_process_management_scenario: TypeProcessManagementScenarioCreator,
      scenario: ProcessManagementScenario,
  ) -> None:
    scenario_mocks = setup_process_management_scenario(scenario)

    supervisor_process_instance.process(scenario_mocks.mocked_task)

    assert mocked_stream.getvalue() == (
        self.log_message_prefix + self.log_message_supervisor_management +
        self.log_message_suffix
    ).format(task=scenario_mocks.mocked_task)

  @pytest.mark.parametrize(
      "scenario", [
          ProcessManagementScenario(
              process=ProcessList.CAMERA,
              requested_state=ProcessStatus.STOPPED,
              process_exception=None,
              method_name="stop"
          ),
          ProcessManagementScenario(
              process=ProcessList.CONTACT_SWITCH_MONITOR,
              requested_state=ProcessStatus.RUNNING,
              process_exception=None,
              method_name="start"
          )
      ]
  )
  def test_process__vary_process__vary_state__successful__calls_process_method(
      self,
      supervisor_process_instance: ProcessorClass,
      setup_process_management_scenario: TypeProcessManagementScenarioCreator,
      scenario: ProcessManagementScenario,
  ) -> None:
    scenario_mocks = setup_process_management_scenario(scenario)

    supervisor_process_instance.process(scenario_mocks.mocked_task)

    scenario_mocks.mocked_supervisor_process.assert_called_once_with(
        scenario_mocks.mocked_task.args.process
    )
    getattr(
        scenario_mocks.mocked_supervisor_process.return_value,
        scenario.method_name
    ).assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario", [
          ProcessManagementScenario(
              process=ProcessList.CAMERA,
              requested_state=ProcessStatus.STOPPED,
              process_exception=SupervisorProcessException,
              method_name="stop"
          ),
          ProcessManagementScenario(
              process=ProcessList.CONTACT_SWITCH_MONITOR,
              requested_state=ProcessStatus.RUNNING,
              process_exception=SupervisorProcessException,
              method_name="start"
          )
      ]
  )
  def test_process__vary_process__vary_state__exception__logging(
      self,
      supervisor_process_instance: ProcessorClass,
      mocked_stream: StringIO,
      setup_process_management_scenario: TypeProcessManagementScenarioCreator,
      scenario: ProcessManagementScenario,
  ) -> None:
    scenario_mocks = setup_process_management_scenario(scenario)

    supervisor_process_instance.process(scenario_mocks.mocked_task)

    assert mocked_stream.getvalue() == (
        self.log_message_prefix + self.log_message_supervisor_management +
        self.log_message_supervisor_management_failed + self.log_message_suffix
    ).format(task=scenario_mocks.mocked_task)

  @pytest.mark.parametrize(
      "scenario", [
          ProcessManagementScenario(
              process=ProcessList.CAMERA,
              requested_state=ProcessStatus.STOPPED,
              process_exception=SupervisorProcessException,
              method_name="stop"
          ),
          ProcessManagementScenario(
              process=ProcessList.CONTACT_SWITCH_MONITOR,
              requested_state=ProcessStatus.RUNNING,
              process_exception=SupervisorProcessException,
              method_name="start"
          )
      ]
  )
  def test_process__vary_process__vary_state__exception__calls_process_method(
      self,
      supervisor_process_instance: ProcessorClass,
      setup_process_management_scenario: TypeProcessManagementScenarioCreator,
      scenario: ProcessManagementScenario,
  ) -> None:
    scenario_mocks = setup_process_management_scenario(scenario)

    supervisor_process_instance.process(scenario_mocks.mocked_task)

    scenario_mocks.mocked_supervisor_process.assert_called_once_with(
        scenario_mocks.mocked_task.args.process
    )
    getattr(
        scenario_mocks.mocked_supervisor_process.return_value,
        scenario.method_name
    ).assert_called_once_with()
