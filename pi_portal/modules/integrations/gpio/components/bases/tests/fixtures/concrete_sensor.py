"""ConcreteGPIOSensor class."""

import random
import time
from typing import Any, Callable

from pi_portal.modules.integrations.gpio.components.bases import \
    sensor as gpio_sensor


class ConcreteGPIOSensor(gpio_sensor.GPIOSensorBase):
  """Concrete implementation of the GPIOSensorBase class."""

  def hook_setup_hardware(self) -> Any:
    random.seed(time.time_ns())
    random_number_generator: Callable[...,int] = \
      lambda: random.randrange(90, 100)
    return random_number_generator

  def hook_update_state(self) -> Any:
    return self.hardware()
