"""TaskSchedulerUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class TaskSchedulerUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the TASK_SCHEDULER process."""

  process_name = supervisor_config.ProcessList.TASK_SCHEDULER
