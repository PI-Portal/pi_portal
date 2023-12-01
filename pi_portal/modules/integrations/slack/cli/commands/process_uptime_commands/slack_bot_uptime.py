"""BotUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from ..bases.process_uptime_command import SlackProcessUptimeCommandBase


class BotUptimeCommand(SlackProcessUptimeCommandBase):
  """Retrieves uptime for the BOT process."""

  process_name = supervisor_config.ProcessList.BOT
