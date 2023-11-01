"""TemperatureMonitorFactory class."""

from pi_portal.modules.integrations.gpio.components import temperature_monitor
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from . import temperature_sensor_factory
from .bases import monitor_factory


class TemperatureMonitorFactory(
    monitor_factory.MonitorFactoryBase[temperature_sensor.TemperatureSensor]
):
  """Factory for TemperatureMonitor instances."""

  def create(self) -> temperature_monitor.TemperatureSensorMonitor:
    """Generate a configured TemperatureMonitor from user configuration.

    :returns: A fully configured TemperatureMonitor.
    """

    sensor_factory = temperature_sensor_factory.TemperatureSensorFactory()
    sensors = sensor_factory.create()

    return temperature_monitor.TemperatureSensorMonitor(sensors)
