"""Test the TempMonitorUptimeCommand class."""

from unittest import mock

from pi_portal.modules.system import supervisor_config
from ..bases import process_uptime_subcommand
from ..uptime_temp_monitor import TempMonitorUptimeCommand


class TestTempMonitorUptimeCommand:
  """Test the TempMonitorUptimeCommand class."""

  def test_initialize__attributes(
      self,
      uptime_temp_monitor_instance: TempMonitorUptimeCommand,
  ) -> None:
    assert uptime_temp_monitor_instance.process_name == (
        supervisor_config.ProcessList.TEMP_MONITOR
    )

  def test_initialize__inheritance(
      self,
      uptime_temp_monitor_instance: TempMonitorUptimeCommand,
  ) -> None:
    assert isinstance(
        uptime_temp_monitor_instance,
        process_uptime_subcommand.ChatProcessUptimeCommandBase,
    )

  def test_initialize__bot(
      self,
      uptime_temp_monitor_instance: TempMonitorUptimeCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert uptime_temp_monitor_instance.chatbot == mocked_chat_bot

  def test_initialize__supervisor_process(
      self,
      uptime_temp_monitor_instance: TempMonitorUptimeCommand,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert uptime_temp_monitor_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        uptime_temp_monitor_instance.process_name
    )
