"""ContactSwitch class."""

from typing import Any

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from pi_portal.modules.integrations.gpio.shim import RPi


class ContactSwitch(gpio_input.GPIOInputBase):
  """GPIO input for a door contact switch.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this door in alerts and logs.
  :param initial_state: The value to initially set the state to.
  """

  open = 1

  def hook_setup_input(self) -> None:
    """Initialize the GPIO input."""

    RPi.GPIO.setup(self.pin_number, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

  def hook_update_state(self) -> Any:
    """Retrieve new state for the GPIO input.

    :returns: The new GPIO state value.
    """

    return RPi.GPIO.input(self.pin_number) == self.open
