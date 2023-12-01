"""Test the TempMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import temp_monitor_uptime


class TestTempMonitorUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the TempMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.TEMP_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = temp_monitor_uptime.TempMonitorUptimeCommand
