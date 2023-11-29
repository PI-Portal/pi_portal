"""TemperatureMonitorLogFileReader class."""

from typing import Any, Dict, List, cast

from pi_portal import config
from pi_portal.modules.configuration import state, user_config
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from pi_portal.modules.mixins import read_log_file

TemperatureReadingType = Dict[str, temperature_sensor.TypeTemperatureData]


class TemperatureMonitorLogFileReader(read_log_file.LogFileReader):
  """Read access to the Temperature Monitor Log File."""

  configured_sensor_count: int
  log_file_path: str = config.TEMPERATURE_MONITOR_LOGFILE_PATH
  temperature_readings: Dict[str, TemperatureReadingType]

  def __init__(self) -> None:
    self.state = state.State()
    self._initialize()

  def _initialize(self) -> None:
    self.temperature_readings: Dict[str, TemperatureReadingType] = {}
    self.configured_sensor_count = 0
    generic_sensor_config = cast(
        Dict[str, List[user_config.TypeUserConfigGPIO]],
        self.state.user_config["TEMPERATURE_SENSORS"],
    )

    for sensor_type, sensor_config in generic_sensor_config.items():
      self.configured_sensor_count += len(sensor_config)
      sensor_type_readings: TemperatureReadingType = {}
      for sensor in sensor_config:
        sensor_name = sensor["NAME"]
        sensor_type_readings[sensor_name] = temperature_sensor.EMPTY_READING
      self.temperature_readings[sensor_type] = sensor_type_readings

  def read_last_values(self) -> Dict[str, TemperatureReadingType]:
    """Parse the log for temperature data, and return the latest record values.

    If no values are found `None` is returned for both humidity and temperature.

    :returns: A temperature readings dictionary keyed by sensor type and name.
    """

    log_data = self.tail(self.configured_sensor_count * 2)
    for json_log_line in log_data:
      self._parse_log_line(json_log_line)
    return self.temperature_readings

  def _parse_log_line(self, json_log_line: Dict[Any, Any]) -> None:
    try:
      sensor_type = json_log_line["sensor_type"]
      sensor_name = json_log_line["sensor_name"]
      humidity = json_log_line["humidity"]
      temperature = json_log_line["temperature"]
      self.temperature_readings[sensor_type][sensor_name] = \
          temperature_sensor.TypeTemperatureData(
            humidity=humidity,
            temperature=temperature
          )
    except (TypeError, KeyError):
      pass
