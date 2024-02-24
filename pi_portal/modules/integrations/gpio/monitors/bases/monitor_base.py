"""GPIOMonitorBase class."""

import abc
import time
from typing import Any, Generic, Sequence, TypeVar

from pi_portal.modules.integrations.chat.service_client import ChatClient
from pi_portal.modules.integrations.gpio.components.bases import \
    input_base as gpio_input
from pi_portal.modules.mixins import write_archived_log_file
from pi_portal.modules.python.rpi import RPi

TypeGenericGpio = TypeVar(
    'TypeGenericGpio',
    bound=gpio_input.GPIOInputBase[Any],
)


class GPIOMonitorBase(
    abc.ABC,
    write_archived_log_file.ArchivedLogFileWriter,
    Generic[TypeGenericGpio],
):
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
    self.chat_client = ChatClient()
    self.gpio_pins = gpio_pins
    self.hook_setup_gpio()

  def start(self) -> None:
    """Begin the monitoring loop."""

    while True:
      self._update_state()
      self._check_state_for_changes()
      time.sleep(self.gpio_poll_interval)

  def _update_state(self) -> None:
    """Poll GPIO and update the known state."""

    for gpio_pin in self.gpio_pins:
      gpio_pin.poll()

  def _check_state_for_changes(self) -> None:
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
