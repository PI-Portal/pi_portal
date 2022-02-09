"""CLI command to start the Door Monitor."""

from pi_portal.modules.integrations import gpio
from .bases import command
from .mixins import state


class DoorMonitorCommand(command.CommandBase, state.CommandManagedStateMixin):
  """CLI command to start the Door Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    factory = gpio.DoorMonitorFactory()
    door_monitor = factory.create()
    door_monitor.start()
