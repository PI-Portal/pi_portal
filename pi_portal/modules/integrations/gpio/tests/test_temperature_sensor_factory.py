"""Test the TemperatureSensorFactory class."""

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.bases.tests.fixtures import (
    sensor_factory_harness,
)
from pi_portal.modules.integrations.gpio.components import dht11_sensor
from .. import temperature_sensor_factory


class TestTemperatureSensorFactory(
    sensor_factory_harness.GPIOSensorFactoryTestHarness
):
  """Test the TemperatureSensorFactory class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = temperature_sensor_factory.TemperatureSensorFactory

  @mock_state.patch
  def test_dht11(self) -> None:
    dht11_config_count = len(
        self.factory.state.user_config["TEMPERATURE_SENSORS"]["DHT11"]
    )
    dht11_created_count = 0
    dht11_identified_count = 0
    for sensor in self.instance:
      if isinstance(sensor, dht11_sensor.DHT11):
        dht11_created_count += 1
        for config in (
            self.factory.state.user_config["TEMPERATURE_SENSORS"]["DHT11"]
        ):
          match_name = config["NAME"] == sensor.pin_name
          match_pin = config["GPIO"] == sensor.pin_number
          if match_name and match_pin:
            dht11_identified_count += 1
            break
    self.assertEqual(dht11_config_count, dht11_created_count)
    self.assertEqual(dht11_config_count, dht11_identified_count)
