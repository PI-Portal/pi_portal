"""CLI command to start the Door Monitor."""

from pi_portal.modules.integrations import gpio
from .bases import command


class DoorMonitorCommand(command.CommandBase):
  """CLI command to start the Door Monitor."""

  def invoke(self) -> None:
    """Invoke the command."""

    factory = gpio.DoorMonitorFactory()
    door_monitor = factory.create()
    door_monitor.start()
