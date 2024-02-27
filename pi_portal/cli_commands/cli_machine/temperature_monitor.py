"""CLI command to start the Temperature Monitor."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import require_task_scheduler, state
from pi_portal.modules.integrations import gpio


class TemperatureMonitorCommand(
    require_task_scheduler.CommandTaskSchedulerMixin,
    state.CommandManagedStateMixin,
    command.CommandBase,
):
  """CLI command to start the Temperature Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    self.require_task_scheduler()

    factory = gpio.TemperatureSensorMonitorFactory()
    temperature_monitor = factory.create()
    temperature_monitor.start()
