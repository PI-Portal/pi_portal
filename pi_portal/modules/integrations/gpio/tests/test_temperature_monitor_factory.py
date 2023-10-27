"""Test the TemperatureMonitorFactory class."""

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.bases.tests.fixtures import (
    monitor_factory_harness,
)
from pi_portal.modules.integrations.gpio.components import temperature_monitor
from .. import temperature_monitor_factory


class TestTemperatureMonitorFactory(
    monitor_factory_harness.GPIOMonitorFactoryTestHarness
):
  """Test the TemperatureMonitorFactory class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = temperature_monitor_factory.TemperatureMonitorFactory
    cls.gpio_input_type = temperature_monitor.TemperatureSensorMonitor

  @mock_state.patch
  def test_gpio(self) -> None:
    self.assertEqual(
        self.instance.gpio_pins[0].pin_name,
        self.factory.state.user_config["TEMPERATURE_SENSORS"]['DHT11'][0]
        ["NAME"]
    )
    self.assertEqual(
        self.instance.gpio_pins[0].pin_number,
        self.factory.state.user_config["TEMPERATURE_SENSORS"]['DHT11'][0]
        ["GPIO"]
    )
