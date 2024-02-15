"""TemperatureSensorMonitorFactory class."""

from typing import List

from pi_portal.modules.integrations.gpio.components.factories import (
    dht11_sensor_factory,
)
from pi_portal.modules.integrations.gpio.monitors import (
    temperature_sensor_monitor,
)
from ...components.bases.temperature_sensor_base import (
    TypeGenericTemperateSensor,
)
from .bases import monitor_factory_base


class TemperatureSensorMonitorFactory(
    monitor_factory_base.MonitorFactoryBase[TypeGenericTemperateSensor]
):
  """Factory for TemperatureSensorMonitor instances."""

  def create(self) -> temperature_sensor_monitor.TemperatureSensorMonitor:
    """Generate a configured TemperatureMonitor from user configuration.

    :returns: A fully configured TemperatureMonitor.
    """

    temperature_sensors: List[TypeGenericTemperateSensor] = []
    dht11_factory = dht11_sensor_factory.DHT11Factory()
    temperature_sensors += dht11_factory.create()

    return temperature_sensor_monitor.TemperatureSensorMonitor(
        temperature_sensors
    )
