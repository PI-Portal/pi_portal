"""Test the ContactSwitchMonitorUptimeCommand class."""

from unittest import mock

from pi_portal.modules.system import supervisor_config
from ..bases import process_uptime_subcommand
from ..uptime_contact_switch_monitor import ContactSwitchMonitorUptimeCommand


class TestContactSwitchMonitorUptimeCommand:
  """Test the ContactSwitchMonitorUptimeCommand class."""

  def test_initialize__attributes(
      self,
      uptime_contact_switch_monitor_instance: ContactSwitchMonitorUptimeCommand,
  ) -> None:
    assert uptime_contact_switch_monitor_instance.process_name == (
        supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR
    )

  def test_initialize__inheritance(
      self,
      uptime_contact_switch_monitor_instance: ContactSwitchMonitorUptimeCommand,
  ) -> None:
    assert isinstance(
        uptime_contact_switch_monitor_instance,
        process_uptime_subcommand.ChatProcessUptimeCommandBase,
    )

  def test_initialize__bot(
      self,
      uptime_contact_switch_monitor_instance: ContactSwitchMonitorUptimeCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert uptime_contact_switch_monitor_instance.chatbot == mocked_chat_bot

  def test_initialize__supervisor_process(
      self,
      uptime_contact_switch_monitor_instance: ContactSwitchMonitorUptimeCommand,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert uptime_contact_switch_monitor_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        uptime_contact_switch_monitor_instance.process_name
    )
