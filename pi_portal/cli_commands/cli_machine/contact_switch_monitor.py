"""CLI command to start the Contact Switch Monitor."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import require_task_scheduler, state
from pi_portal.modules.integrations import gpio


class ContactSwitchMonitorCommand(
    require_task_scheduler.CommandTaskSchedulerMixin,
    state.CommandManagedStateMixin,
    command.CommandBase,
):
  """CLI command to start the Contact Switch Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    self.require_task_scheduler()

    factory = gpio.ContactSwitchMonitorFactory()
    contact_switch_monitor = factory.create()
    contact_switch_monitor.start()
