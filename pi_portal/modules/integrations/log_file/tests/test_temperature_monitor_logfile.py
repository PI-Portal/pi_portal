"""Test the TemperatureMonitorLogFileReader class."""

import json
import os
from unittest import mock

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from pi_portal.modules.mixins import read_log_file
from ..temperature_monitor_logfile import TemperatureMonitorLogFileReader

READ_LOG_FILE_MODULE = read_log_file.__name__


class TestTemperatureMonitorLogFileReader:
  """Test the TemperatureMonitorLogFileReader class."""

  @property
  def mock_empty_file(self) -> mock.Mock:
    return mock.Mock(return_value=[])

  @property
  def mock_one_sensor_file(self) -> mock.Mock:
    data = []
    with open(
        os.path.dirname(__file__) +
        "/fixtures/mock_temperature_log_file__one_sensor.txt",
        "r",
        encoding="utf-8",
    ) as file_handle:
      for line in file_handle.readlines():
        data.append(json.loads(line))
    return mock.Mock(return_value=data)

  @property
  def mock_two_sensors_file(self) -> mock.Mock:
    data = []
    with open(
        os.path.dirname(__file__) +
        "/fixtures/mock_temperature_log_file__two_sensors.txt",
        "r",
        encoding="utf-8",
    ) as file_handle:
      for line in file_handle.readlines():
        data.append(json.loads(line))
    return mock.Mock(return_value=data)

  @property
  def mock_two_sensors_corrupt_file(self) -> mock.Mock:
    data = TestTemperatureMonitorLogFileReader().mock_two_sensors_file
    data.return_value[2] = "{ NOT VALID JSON"
    data.return_value[4] = "{ NOT VALID JSON"
    return data

  def test_initialization__one_sensor(
      self,
      mocked_state: state.State,
      one_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    assert one_sensor_temp_log_file_reader.log_file_path == \
           config.TEMPERATURE_MONITOR_LOGFILE_PATH
    assert one_sensor_temp_log_file_reader.state.user_config == \
           mocked_state.user_config
    assert one_sensor_temp_log_file_reader.configured_sensor_count == 1
    assert one_sensor_temp_log_file_reader.temperature_readings == {
        'DHT11': {
            'Kitchen': {
                'temperature': None,
                'humidity': None
            }
        }
    }

  def test_initialization__two_sensors(
      self,
      mocked_state: state.State,
      two_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    assert two_sensor_temp_log_file_reader.log_file_path == \
           config.TEMPERATURE_MONITOR_LOGFILE_PATH
    assert two_sensor_temp_log_file_reader.state.user_config == \
           mocked_state.user_config
    assert two_sensor_temp_log_file_reader.configured_sensor_count == 2
    assert two_sensor_temp_log_file_reader.temperature_readings == {
        'DHT11':
            {
                'Bedroom': {
                    'temperature': None,
                    'humidity': None
                },
                'Kitchen': {
                    'temperature': None,
                    'humidity': None
                }
            }
    }

  @mock.patch(READ_LOG_FILE_MODULE + ".LogFileReader.tail", mock_empty_file)
  def test_read_last_values__one_sensor__empty_file__empty_reading(
      self,
      one_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    result = one_sensor_temp_log_file_reader.read_last_values()

    assert result == {
        'DHT11': {
            'Kitchen': {
                'temperature': None,
                'humidity': None
            }
        }
    }

  @mock.patch(READ_LOG_FILE_MODULE + ".LogFileReader.tail", mock_empty_file)
  def test_read_last_values__two_sensors__empty_file__empty_readings(
      self,
      two_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    result = two_sensor_temp_log_file_reader.read_last_values()

    assert result == {
        'DHT11':
            {
                'Bedroom': {
                    'temperature': None,
                    'humidity': None
                },
                'Kitchen': {
                    'temperature': None,
                    'humidity': None
                }
            }
    }

  @mock.patch(
      READ_LOG_FILE_MODULE + ".LogFileReader.tail", mock_one_sensor_file
  )
  def test_read_last_values__one_sensor__populated_file__populated_reading(
      self,
      one_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    result = one_sensor_temp_log_file_reader.read_last_values()

    assert result == {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor.TypeTemperatureData(
                        humidity=38,
                        temperature=22,
                    )
            }
    }

  @mock.patch(
      READ_LOG_FILE_MODULE + ".LogFileReader.tail", mock_two_sensors_file
  )
  def test_read_last_values__two_sensors__populated_file__populated_reading(
      self,
      two_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    result = two_sensor_temp_log_file_reader.read_last_values()

    assert result == {
        "DHT11":
            {
                'Bedroom':
                    temperature_sensor.TypeTemperatureData(
                        humidity=39,
                        temperature=23,
                    ),
                "Kitchen":
                    temperature_sensor.TypeTemperatureData(
                        humidity=38,
                        temperature=22,
                    )
            }
    }

  @mock.patch(
      READ_LOG_FILE_MODULE + ".LogFileReader.tail",
      mock_two_sensors_corrupt_file
  )
  def test_read_last_values__one_sensors__corrupt_file__partial_readings(
      self,
      two_sensor_temp_log_file_reader: TemperatureMonitorLogFileReader,
  ) -> None:
    result = two_sensor_temp_log_file_reader.read_last_values()

    assert result == {
        "DHT11":
            {
                'Bedroom':
                    temperature_sensor.TypeTemperatureData(
                        humidity=37,
                        temperature=21,
                    ),
                "Kitchen":
                    temperature_sensor.TypeTemperatureData(
                        humidity=38,
                        temperature=22,
                    )
            }
    }
