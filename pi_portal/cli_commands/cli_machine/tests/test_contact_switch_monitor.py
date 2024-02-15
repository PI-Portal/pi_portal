"""Test the ContactSwitchMonitorCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine.contact_switch_monitor import (
    ContactSwitchMonitorCommand,
)
from pi_portal.cli_commands.mixins import state


class TestContactSwitchMonitorCommand:
  """Test the ContactSwitchMonitorCommand class."""

  def test_initialize__inheritance(
      self,
      contact_switch_monitor_command_instance: ContactSwitchMonitorCommand,
  ) -> None:
    assert isinstance(
        contact_switch_monitor_command_instance, command.CommandBase
    )
    assert isinstance(
        contact_switch_monitor_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      contact_switch_monitor_command_instance: ContactSwitchMonitorCommand,
      mocked_contact_switch_monitor_factory: mock.Mock,
  ) -> None:
    contact_switch_monitor_command_instance.invoke()

    m_factory_instance = mocked_contact_switch_monitor_factory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    mocked_contact_switch_monitor_factory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()
