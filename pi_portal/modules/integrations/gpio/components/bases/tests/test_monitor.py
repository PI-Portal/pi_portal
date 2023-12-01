"""Test the GPIOMonitorBase Class."""

from unittest import mock

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from pi_portal.modules.integrations.gpio.components.bases import monitor
from .fixtures import (
    concrete_input,
    concrete_monitor,
    gpio_change,
    gpio_loop,
    monitor_harness,
)


class TestConcreteGPIOMonitor(
    monitor_harness.GPIOMonitorTestHarness[gpio_input.GPIOInputBase,
                                           concrete_monitor.ConcreteGPIOMonitor]
):
  """Test the GPIOMonitorBase class with a concrete implementation."""

  __test__ = True

  gpio_input_1 = concrete_input.ConcreteGPIOInput(1, "test1", 1)
  gpio_input_2 = concrete_input.ConcreteGPIOInput(2, "test2", 1)

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = concrete_monitor.ConcreteGPIOMonitor

  @gpio_loop.patch_gpio_loop(monitor.__name__ + ".GPIOMonitorBase")
  @mock.patch(monitor.__name__ + ".RPi.GPIO", mock.Mock())
  def test_loop_no_change(self) -> None:

    with gpio_change.patch_gpio_input_change(self.instance.gpio_pins, False):
      mock_logger_message = "No New Messages"

      with self.assertLogs(self.instance.log, level='DEBUG') as logs:
        self.instance.log.info(mock_logger_message)
        self.instance.start()

      self.assertListEqual(
          logs.output,
          [f"INFO:{self.instance.logger_name}:{mock_logger_message}"]
      )

  @gpio_loop.patch_gpio_loop(monitor.__name__ + ".GPIOMonitorBase")
  @mock.patch(monitor.__name__ + ".RPi.GPIO", mock.Mock())
  def test_loop_when_logging_all_states(self) -> None:
    self.instance.gpio_log_changes_only = False
    with gpio_change.patch_gpio_input_change(self.instance.gpio_pins, False):
      mock_logger_message = "No New Messages"

      with self.assertLogs(self.instance.log, level='DEBUG') as logs:
        self.instance.log.info(mock_logger_message)
        self.instance.start()

      self.assertListEqual(
          logs.output, [
              f"INFO:{self.instance.logger_name}:{mock_logger_message}",
              (
                  f"ERROR:{self.instance.logger_name}:"
                  f"{self.gpio_input_1.pin_name}"
              ),
              (
                  f"ERROR:{self.instance.logger_name}:"
                  f"{self.gpio_input_2.pin_name}"
              ),
          ]
      )

  @gpio_loop.patch_gpio_loop(monitor.__name__ + ".GPIOMonitorBase")
  @mock.patch(monitor.__name__ + ".RPi.GPIO", mock.Mock())
  def test_loop_with_change(self) -> None:

    with gpio_change.patch_gpio_input_change(self.instance.gpio_pins, True):
      mock_logger_message = "No New Messages"

      with self.assertLogs(self.instance.log, level='DEBUG') as logs:
        self.instance.log.info(mock_logger_message)
        self.instance.start()

      self.assertListEqual(
          logs.output, [
              f"INFO:{self.instance.logger_name}:{mock_logger_message}",
              (
                  f"ERROR:{self.instance.logger_name}:"
                  f"{self.gpio_input_1.pin_name}"
              ),
              (
                  f"ERROR:{self.instance.logger_name}:"
                  f"{self.gpio_input_2.pin_name}"
              ),
          ]
      )
