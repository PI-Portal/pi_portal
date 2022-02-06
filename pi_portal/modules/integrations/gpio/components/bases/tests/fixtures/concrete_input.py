"""ConcreteGPIOInput class."""

from typing import Any

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input


class ConcreteGPIOInput(gpio_input.GPIOInputBase):
  """Concrete implementation of the GPIOInputBase class."""

  def hook_update_state(self) -> Any:
    return self.last_state + 1
