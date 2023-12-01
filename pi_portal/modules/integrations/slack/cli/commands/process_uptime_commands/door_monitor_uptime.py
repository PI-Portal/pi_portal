"""DoorMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class DoorMonitorUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the DOOR_MONITOR process."""

  process_name = supervisor_config.ProcessList.DOOR_MONITOR
