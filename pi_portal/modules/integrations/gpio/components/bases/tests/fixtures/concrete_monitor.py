"""ConcreteGPIOMonitor class."""

from ... import input as gpio_input
from ... import monitor


class ConcreteGPIOMonitor(monitor.GPIOMonitorBase[gpio_input.GPIOInputBase]):
  """Concrete implementation of the GPIOMonitorBase class."""

  gpio_log_changes_only = True
  logger_name = "test_logger"
  log_file_path = "test.log"
  gpio_poll_interval = 0.01

  def hook_log_state(self, gpio_pin: gpio_input.GPIOInputBase) -> None:
    self.log.error(gpio_pin.pin_name)
