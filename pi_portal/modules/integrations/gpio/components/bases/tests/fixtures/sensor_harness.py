"""GPIO sensor test harness."""

import abc
from typing import Any, Type, cast

from pi_portal.modules.integrations.gpio.components.bases import \
    sensor as gpio_sensor
from . import input_harness


class GPIOSensorTestHarness(input_harness.GPIOInputTestHarness, abc.ABC):
  """Test harness for the GPIOInputBase class."""

  __test__ = False
  gpio_input_1_name = "test_pin_1"
  gpio_input_1_pin = 1
  gpio_input_1_initial_value: Any = 1
  test_class: Type[gpio_sensor.GPIOSensorBase]

  def get_instance(self) -> gpio_sensor.GPIOSensorBase:
    return cast(gpio_sensor.GPIOSensorBase, self.instance)

  @abc.abstractmethod
  def test_hook_setup_hardware(self) -> None:
    """Override to test the hook_setup_hardware method."""

  @abc.abstractmethod
  def test_poll(self) -> None:
    """Override to test the poll method."""
