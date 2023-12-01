"""CronVideosUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class CronVideosUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the CRON_VIDEO process."""

  process_name = supervisor_config.ProcessList.CRON_VIDEOS
