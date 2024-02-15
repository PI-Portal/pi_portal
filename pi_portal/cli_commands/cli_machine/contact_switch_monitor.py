"""CLI command to start the Contact Switch Monitor."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import state
from pi_portal.modules.integrations import gpio


class ContactSwitchMonitorCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the Contact Switch Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    factory = gpio.ContactSwitchMonitorFactory()
    contact_switch_monitor = factory.create()
    contact_switch_monitor.start()
