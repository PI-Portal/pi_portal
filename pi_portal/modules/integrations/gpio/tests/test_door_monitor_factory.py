"""Test the DoorMonitorFactory class."""

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.bases.tests.fixtures import (
    monitor_factory_harness,
)
from pi_portal.modules.integrations.gpio.components import (
    contact_switch,
    door_monitor,
)
from .. import door_monitor_factory


class TestDoorMonitorFactory(
    monitor_factory_harness.GPIOMonitorFactoryTestHarness[
        contact_switch.ContactSwitch]
):
  """Test the DoorMonitorFactory class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = door_monitor_factory.DoorMonitorFactory
    cls.gpio_input_type = door_monitor.DoorMonitor

  @mock_state.patch
  def test_gpio(self) -> None:
    self.assertEqual(
        self.instance.gpio_pins[0].pin_name,
        self.factory.state.user_config["SWITCHES"]['CONTACT_SWITCHES'][0]
        ["NAME"]
    )
    self.assertEqual(
        self.instance.gpio_pins[0].pin_number,
        self.factory.state.user_config["SWITCHES"]['CONTACT_SWITCHES'][0]
        ["GPIO"]
    )
