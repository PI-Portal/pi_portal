"""GPIOMonitorBase class."""

import abc
import time
from typing import Generic, Sequence, TypeVar

from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from pi_portal.modules.integrations.gpio.shim import RPi
from pi_portal.modules.integrations.slack import client
from pi_portal.modules.mixins import log_file

TypeGenericGpio = TypeVar('TypeGenericGpio', bound=gpio_input.GPIOInputBase)


class GPIOMonitorBase(abc.ABC, log_file.WriteLogFile, Generic[TypeGenericGpio]):
  """GPIO input monitor class.

  :param gpio_pins: A list of GPIO Inputs to monitor.
  """

  gpio_poll_interval = 0.5
  gpio_log_changes_only: bool
  gpio_pins: Sequence[TypeGenericGpio]
  logger_name: str
  log_file_path: str

  def __init__(self, gpio_pins: Sequence[TypeGenericGpio]) -> None:
    self.configure_logger()
    self.slack_client = client.SlackClient()
    self.gpio_pins = gpio_pins
    self.hook_setup_gpio()

  def start(self) -> None:
    """Begin the monitoring loop."""

    while self.is_running():
      self.update_state()
      self.check_state_for_changes()
      time.sleep(self.gpio_poll_interval)

  def is_running(self) -> bool:
    """Indicate if the polling loop is active.  Override for testing."""

    return True

  def update_state(self) -> None:
    """Poll GPIO and update the known state for the doors."""

    for gpio_pin in self.gpio_pins:
      gpio_pin.poll()

  def check_state_for_changes(self) -> None:
    """Log any detected differences in state."""

    for gpio_pin in self.gpio_pins:
      if not self.gpio_log_changes_only or gpio_pin.has_changed():
        self.hook_log_state(gpio_pin)

  def hook_setup_gpio(self) -> None:
    """Initialize the GPIO mode, specific to the RPi library."""

    RPi.GPIO.setmode(RPi.GPIO.BCM)

  @abc.abstractmethod
  def hook_log_state(self, gpio_pin: TypeGenericGpio) -> None:
    """Override to log customized messages about a GPIO input state.

    :param gpio_pin: A GPIO pin to log an event for.
    """
