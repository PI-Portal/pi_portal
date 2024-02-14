"""Test fixtures for the log_file modules tests."""

import pytest
from pi_portal.modules.configuration import state
from ..temperature_monitor_logfile import TemperatureMonitorLogFileReader


@pytest.fixture
def one_sensor_temp_log_file_reader() -> TemperatureMonitorLogFileReader:
  """Test double for the temperature monitor logfile."""
  return TemperatureMonitorLogFileReader()


@pytest.fixture
def two_sensor_temp_log_file_reader(
    test_state: state.State,
) -> TemperatureMonitorLogFileReader:
  """Test double for the temperature monitor logfile."""
  test_state.user_config["TEMPERATURE_SENSORS"]["DHT11"].append(
      {
          "GPIO": 1,
          "NAME": "Bedroom"
      }
  )
  return TemperatureMonitorLogFileReader()
