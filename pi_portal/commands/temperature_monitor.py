"""CLI command to start the Temperature Monitor."""

from pi_portal.modules.integrations import gpio
from .bases import command
from .mixins import state


class TemperatureMonitorCommand(
    command.CommandBase, state.CommandManagedStateMixin
):
  """CLI command to start the Temperature Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    factory = gpio.TemperatureMonitorFactory()
    temperature_monitor = factory.create()
    temperature_monitor.start()
