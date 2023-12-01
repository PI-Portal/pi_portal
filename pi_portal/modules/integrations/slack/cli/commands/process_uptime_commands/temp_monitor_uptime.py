"""TempMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class TempMonitorUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the TEMP_MONITOR process."""

  process_name = supervisor_config.ProcessList.TEMP_MONITOR
