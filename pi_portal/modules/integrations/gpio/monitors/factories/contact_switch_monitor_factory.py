"""ContactSwitchMonitorFactory class."""

from typing import List

from pi_portal.modules.integrations.gpio.components import contact_switch
from pi_portal.modules.integrations.gpio.components.factories import (
    contact_switch_factory,
)
from pi_portal.modules.integrations.gpio.monitors import contact_switch_monitor
from .bases import monitor_factory_base


class ContactSwitchMonitorFactory(
    monitor_factory_base.MonitorFactoryBase[contact_switch.ContactSwitch]
):
  """Factory for ContactSwitchMonitor instances."""

  def create(self) -> contact_switch_monitor.ContactSwitchMonitor:
    """Generate a configured ContactSwitchMonitor from user configuration.

    :returns: A fully configured ContactSwitchMonitor.
    """

    contact_switches: List[contact_switch.ContactSwitch] = []
    switch_factory = contact_switch_factory.ContactSwitchFactory()
    contact_switches += switch_factory.create()

    return contact_switch_monitor.ContactSwitchMonitor(contact_switches)
