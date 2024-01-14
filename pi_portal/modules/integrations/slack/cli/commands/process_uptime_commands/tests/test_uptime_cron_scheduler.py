"""Test the CronSchedulerUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import cron_scheduler_uptime


class TestCronVideosUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the CronSchedulerUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.CRON_SCHEDULER

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = cron_scheduler_uptime.CronSchedulerUptimeCommand
