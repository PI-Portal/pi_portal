"""DoorMonitor class."""

from enum import Enum

from pi_portal import config
from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from pi_portal.modules.integrations.gpio.components.bases import monitor


class DoorState(Enum):
  """States for a door."""

  OPENED = True
  CLOSED = False


class DoorMonitor(monitor.GPIOMonitorBase):
  """Door contact switch monitor and logger.

  :param gpio_pins: A list of GPIO Inputs to monitor.
  """

  gpio_poll_interval = 0.5
  gpio_log_changes_only = True
  logger_name = "pi_portal_door"
  log_file_path = config.DOOR_MONITOR_LOGFILE_PATH
  open = DoorState["OPENED"].value

  def hook_log_state(self, gpio_pin: gpio_input.GPIOInputBase) -> None:
    """Log customized messages when a state change is detected.

    :param gpio_pin: A GPIO pin to log an event for.
    """

    self.log.warning("%s:%s", gpio_pin.pin_name, self._state_name(gpio_pin))
    slack_message = (
        f":rotating_light: The {gpio_pin.pin_name} "
        f"door was {self._state_name(gpio_pin)}!"
    )
    self.slack_client.send_message(slack_message)

  def _state_name(self, gpio_pin: gpio_input.GPIOInputBase) -> str:
    return DoorState(gpio_pin.current_state == self.open).name
