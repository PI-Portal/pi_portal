"""ContactSwitch class."""

from typing import Optional, cast

from pi_portal.modules.integrations.gpio.components.bases import \
    input_base as gpio_input
from pi_portal.modules.python.rpi import RPi


class ContactSwitch(gpio_input.GPIOInputBase[Optional[bool]]):
  """GPIO input for a contact switch."""

  current_state: Optional[bool]
  open = 1

  def __init__(
      self,
      pin_number: int,
      pin_name: str,
  ) -> None:
    super().__init__(pin_number, pin_name, None)

  def hook_setup_input(self) -> None:
    """Initialize the GPIO input."""

    RPi.GPIO.setup(self.pin_number, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

  def hook_update_state(self) -> bool:
    """Retrieve new state for the GPIO input.

    :returns: The new GPIO state value.
    """

    return cast(bool, RPi.GPIO.input(self.pin_number) == self.open)
