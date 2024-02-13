"""Test the DoorMonitorCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine import door_monitor
from pi_portal.cli_commands.mixins import state


class TestDoorMonitorCommand:
  """Test the DoorMonitorCommand class."""

  def test_initialize__inheritance(
      self,
      door_monitor_command_instance: door_monitor.DoorMonitorCommand,
  ) -> None:
    assert isinstance(door_monitor_command_instance, command.CommandBase)
    assert isinstance(
        door_monitor_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      door_monitor_command_instance: door_monitor.DoorMonitorCommand,
      mocked_door_monitor_factory: mock.Mock,
  ) -> None:
    door_monitor_command_instance.invoke()

    m_factory_instance = mocked_door_monitor_factory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    mocked_door_monitor_factory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
