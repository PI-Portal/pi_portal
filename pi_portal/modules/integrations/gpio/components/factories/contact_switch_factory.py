"""ContactSwitchFactory class."""

from typing import List, Optional, Sequence

from pi_portal.modules.integrations.gpio.components import contact_switch
from pi_portal.modules.integrations.gpio.components.factories.bases import (
    input_factory_base,
)


class ContactSwitchFactory(
    input_factory_base.GPIOInputFactoryBase[Optional[bool]]
):
  """Factory for ContactSwitch instances."""

  def create(self) -> Sequence[contact_switch.ContactSwitch]:
    """Generate an array of contact switches from user configuration.

    :returns: An array of contact switches.
    """
    switches: List[contact_switch.ContactSwitch] = []
    for switch in self.state.user_config["SWITCHES"]["CONTACT_SWITCHES"]:
      switches.append(
          contact_switch.ContactSwitch(
              pin_name=switch["NAME"],
              pin_number=switch["GPIO"],
          )
      )
    return switches
