"""CronSchedulerUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class CronSchedulerUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the CRON_SCHEDULER process."""

  process_name = supervisor_config.ProcessList.CRON_SCHEDULER
