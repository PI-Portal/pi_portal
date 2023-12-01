"""Test the DoorMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import door_monitor_uptime


class TestDoorMonitorUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the DoorMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.DOOR_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = door_monitor_uptime.DoorMonitorUptimeCommand
