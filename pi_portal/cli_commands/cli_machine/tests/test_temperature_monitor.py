"""Test the TemperatureMonitorCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine import temperature_monitor
from pi_portal.cli_commands.mixins import require_task_scheduler, state


class TestTemperatureMonitorCommand:
  """Test the TemperatureMonitorCommand class."""

  def test_initialize__inheritance(
      self,
      temperature_monitor_command_instance: temperature_monitor.
      TemperatureMonitorCommand,
  ) -> None:
    assert isinstance(
        temperature_monitor_command_instance,
        require_task_scheduler.CommandTaskSchedulerMixin,
    )
    assert isinstance(
        temperature_monitor_command_instance,
        state.CommandManagedStateMixin,
    )
    assert isinstance(
        temperature_monitor_command_instance,
        command.CommandBase,
    )

  def test_invoke__waits_for_task_scheduler(
      self,
      temperature_monitor_command_instance: temperature_monitor.
      TemperatureMonitorCommand,
      mocked_require_task_scheduler: mock.Mock,
  ) -> None:
    temperature_monitor_command_instance.invoke()

    mocked_require_task_scheduler.assert_called_once_with()

  def test_invoke__starts_temperature_sensor_monitor(
      self,
      temperature_monitor_command_instance: temperature_monitor.
      TemperatureMonitorCommand,
      mocked_temperature_sensor_monitor_factory: mock.Mock,
  ) -> None:
    temperature_monitor_command_instance.invoke()

    m_factory_instance = mocked_temperature_sensor_monitor_factory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    mocked_temperature_sensor_monitor_factory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
