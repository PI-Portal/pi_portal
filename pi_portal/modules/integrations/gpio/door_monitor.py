"""DoorMonitor Class."""

import logging
import os
import sys
import time
from enum import Enum
from typing import Dict, Optional, cast

from pi_portal import config
from pi_portal.modules.integrations import slack

if os.uname()[4][:3] != 'arm':
  import fake_rpi
  sys.modules['RPi'] = fake_rpi.RPi
  sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO

import RPi.GPIO  # pylint: disable=import-error,wrong-import-position

MonitorStateType = Dict[int, Optional[bool]]


class DoorState(Enum):
  """States for a door."""

  OPENED = True
  CLOSED = False


class DoorMonitor:
  """Door state monitor and logger."""

  hardware: Dict[int, int] = config.GPIO_SWITCHES
  running = True
  logger_name = "pi_portal"
  state: MonitorStateType = cast(MonitorStateType, config.GPIO_INITIAL_STATE)
  interval = 0.5
  GPIO = RPi.GPIO
  GPIO_OPEN = True

  def __init__(self):
    self.log = logging.getLogger(self.logger_name)
    self.GPIO.setmode(self.GPIO.BCM)
    for _, pin in self.hardware.items():
      self.GPIO.setup(pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
    self.slack_client = slack.Client()

  def start(self):
    """Begin the monitoring loop."""

    while self.running:
      old_state = dict(self.state)
      self.update_state()
      self.log_state_changes(old_state)
      time.sleep(self.interval)

  def update_state(self):
    """Poll GPIO and update the known state for the doors."""

    for switch, pin in self.hardware.items():
      self.state[switch] = self.GPIO.input(pin) == self.GPIO_OPEN

  def log_state_changes(self, old_state: MonitorStateType):
    """Log any detected differences in state.

    :param old_state: A version of the state to diff against.
    """

    for switch, _ in self.hardware.items():
      new_state = self.state[switch]
      if old_state[switch] != new_state:
        self.log.warning(
            "%s: DOOR %s", self._door_state_name(new_state), switch
        )
        slack_message = (
            f":rotating_light: The {config.DoorNames(switch).name.lower()} "
            f"door was {self._door_state_name(new_state)}!"
        )
        self.slack_client.send_message(slack_message)

  def _door_state_name(self, door_gpio_value: Optional[bool]) -> str:
    return DoorState(door_gpio_value == self.GPIO_OPEN).name
