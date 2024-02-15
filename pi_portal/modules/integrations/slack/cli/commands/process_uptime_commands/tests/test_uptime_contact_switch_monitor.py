"""Test the ContactSwitchMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import contact_switch_monitor_uptime


class TestContactSwitchMonitorUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the ContactSwitchMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = (
        contact_switch_monitor_uptime.ContactSwitchMonitorUptimeCommand
    )
