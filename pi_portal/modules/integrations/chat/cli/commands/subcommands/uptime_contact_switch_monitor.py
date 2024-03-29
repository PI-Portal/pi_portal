"""ContactSwitchMonitorUptimeCommand class."""

from pi_portal.modules.system import supervisor_config
from .bases.process_uptime_subcommand import ChatProcessUptimeCommandBase


class ContactSwitchMonitorUptimeCommand(ChatProcessUptimeCommandBase):
  """Retrieves uptime for the CONTACT_SWITCH_MONITOR process."""

  process_name = supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR
