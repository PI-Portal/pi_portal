"""TemperatureMonitorFactory class."""

from typing import List, Sequence

from pi_portal.modules.integrations.gpio.components import dht11_sensor
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from pi_portal.modules.integrations.gpio.components.factories.bases import (
    temperature_factory_base,
)
from pi_portal.modules.python.rpi import adafruit_dht


class DHT11Factory(
    temperature_factory_base.TemperatureSensorFactoryBase[adafruit_dht.DHT11]
):
  """Factory for DHT11 instances."""

  def create(
      self
  ) -> Sequence[temperature_sensor_base.TypeGenericTemperateSensor]:
    """Generate an array of temperature sensors from user configuration.

    :returns: An array of temperature sensors.
    """
    sensors: List[temperature_sensor_base.TypeGenericTemperateSensor] = []
    for switch in (self.state.user_config["TEMPERATURE_SENSORS"]["DHT11"]):
      sensors.append(
          dht11_sensor.DHT11(
              pin_name=switch["NAME"],
              pin_number=switch["GPIO"],
          )
      )
    return sensors
