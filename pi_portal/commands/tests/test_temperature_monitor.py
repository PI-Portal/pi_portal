"""Test the TemperatureMonitorCommand class."""

from unittest import mock

from .. import temperature_monitor
from ..bases import command
from ..mixins import state


class TestTemperatureMonitorCommand:
  """Test the TemperatureMonitorCommand class."""

  def test_initialize__inheritance(
      self,
      temperature_monitor_command_instance: temperature_monitor.
      TemperatureMonitorCommand,
  ) -> None:
    assert isinstance(temperature_monitor_command_instance, command.CommandBase)
    assert isinstance(
        temperature_monitor_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      temperature_monitor_command_instance: temperature_monitor.
      TemperatureMonitorCommand,
      mocked_temperature_monitor_factory: mock.Mock,
  ) -> None:
    temperature_monitor_command_instance.invoke()

    m_factory_instance = mocked_temperature_monitor_factory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    mocked_temperature_monitor_factory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
