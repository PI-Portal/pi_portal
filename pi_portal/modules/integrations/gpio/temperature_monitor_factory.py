"""TemperatureMonitorFactory class."""

from typing import List

from pi_portal.modules.integrations.gpio.components import (
    dht11_sensor,
    temperature_monitor,
)
from .bases import factory


class TemperatureMonitorFactory(factory.MonitorFactoryBase):
  """Factory for TemperatureMonitor instances."""

  def create(self) -> temperature_monitor.TemperatureSensorMonitor:
    """Generate a configured TemperatureMonitor from user configuration.

    :returns: A fully configured TemperatureMonitor.
    """

    sensors: List[dht11_sensor.DHT11] = []
    for switch in self.state.user_config["DHT11_SENSORS"]:
      sensors.append(
          dht11_sensor.DHT11(
              pin_name=switch["NAME"],
              pin_number=switch["GPIO"],
          )
      )
    return temperature_monitor.TemperatureSensorMonitor(sensors)
