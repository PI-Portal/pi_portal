"""DoorMonitorFactory class."""

from typing import List

from pi_portal.modules.integrations.gpio.components import (
    contact_switch,
    door_monitor,
)
from .bases import MonitorFactoryBase


class DoorMonitorFactory(MonitorFactoryBase):
  """Factory for DoorMonitor instances."""

  def create(self) -> door_monitor.DoorMonitor:
    """Generate a configured DoorMonitor from user configuration.

    :returns: A fully configured DoorMonitor.
    """

    switches: List[contact_switch.ContactSwitch] = []
    for switch in self.state.user_config["CONTACT_SWITCHES"]:
      switches.append(
          contact_switch.ContactSwitch(
              pin_name=switch["NAME"],
              pin_number=switch["GPIO"],
              initial_state=None
          )
      )
    return door_monitor.DoorMonitor(switches)
