"""TemperatureMonitorFactory class."""

from typing import List, Sequence

from pi_portal.modules.integrations.gpio.components import dht11_sensor
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from .bases import sensor_factory


class TemperatureSensorFactory(sensor_factory.SensorFactoryBase):
  """Factory for TemperatureMonitor instances."""

  def create(self) -> Sequence[temperature_sensor.TemperatureSensor]:
    """Generate an array of temperature sensors from user configuration.

    :returns: An array of temperature sensors.
    """
    sensors: List[temperature_sensor.TemperatureSensor] = []
    for switch in (self.state.user_config["TEMPERATURE_SENSORS"]["DHT11"]):
      sensors.append(
          dht11_sensor.DHT11(
              pin_name=switch["NAME"],
              pin_number=switch["GPIO"],
          )
      )
    return sensors
