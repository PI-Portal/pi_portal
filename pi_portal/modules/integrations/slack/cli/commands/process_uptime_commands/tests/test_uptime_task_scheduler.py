"""Test the TaskSchedulerUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ...bases.tests.fixtures import process_uptime_command_harness
from .. import task_scheduler_uptime


class TestTaskSchedulerUptimeCommand(
    process_uptime_command_harness.ProcessUptimeCommandBaseTestHarness
):
  """Test the TaskSchedulerUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.TASK_SCHEDULER

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = task_scheduler_uptime.TaskSchedulerUptimeCommand
