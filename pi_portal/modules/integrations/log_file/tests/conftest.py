"""Test fixtures for the log_file modules tests."""

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state
from ..temperature_monitor_logfile import TemperatureMonitorLogFileReader


@pytest.fixture
@mock_state.patch
def one_sensor_temp_log_file_reader() -> TemperatureMonitorLogFileReader:
  """Test double for the temperature monitor logfile."""
  return TemperatureMonitorLogFileReader()


@pytest.fixture
def two_sensor_temp_log_file_reader(
    mocked_state: state.State
) -> TemperatureMonitorLogFileReader:
  """Test double for the temperature monitor logfile."""
  mocked_state.user_config["TEMPERATURE_SENSORS"]["DHT11"].append(
      {
          "GPIO": 1,
          "NAME": "Bedroom"
      }
  )
  state.State().user_config = mocked_state.user_config
  return TemperatureMonitorLogFileReader()
