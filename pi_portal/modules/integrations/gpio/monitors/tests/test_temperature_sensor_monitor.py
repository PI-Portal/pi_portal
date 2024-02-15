"""Test the TemperatureSensorMonitor class."""
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal import config
from ..bases import monitor_base
from ..temperature_sensor_monitor import TemperatureSensorMonitor
from .conftest import (
    TemperatureSensorScenario,
    generate_temperature_scenario_ids,
)


class TestTemperatureSensorMonitor:
  """Test the TemperatureSensorMonitor class."""

  def test_initialize__attributes(
      self,
      temperature_sensor_monitor_instance: TemperatureSensorMonitor,
      mocked_gpio_pins: List[mock.Mock],
  ) -> None:
    assert temperature_sensor_monitor_instance.gpio_poll_interval == 60.0
    assert temperature_sensor_monitor_instance.gpio_log_changes_only is False
    assert temperature_sensor_monitor_instance.gpio_pins == mocked_gpio_pins
    assert temperature_sensor_monitor_instance.logger_name == "temperature"
    assert temperature_sensor_monitor_instance.log_file_path == (
        config.LOG_FILE_TEMPERATURE_MONITOR
    )

  def test_initialize__inheritance(
      self,
      temperature_sensor_monitor_instance: TemperatureSensorMonitor,
  ) -> None:
    assert isinstance(
        temperature_sensor_monitor_instance,
        monitor_base.GPIOMonitorBase,
    )

  @pytest.mark.usefixtures("temperature_sensor_monitor_instance")
  def test_initialize__rpi_module(
      self,
      mocked_rpi_module: mock.Mock,
  ) -> None:
    mocked_rpi_module.GPIO.setmode.assert_called_once_with(
        mocked_rpi_module.GPIO.BCM
    )

  def test_initialize__slack_client(
      self,
      temperature_sensor_monitor_instance: TemperatureSensorMonitor,
      mocked_slack_client: mock.Mock,
  ) -> None:
    assert temperature_sensor_monitor_instance.slack_client == (
        mocked_slack_client.return_value
    )
    mocked_slack_client.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario",
      [
          TemperatureSensorScenario(
              name="Kitchen",
              type="DHT11",
              state={
                  "temperature": 20,
                  "humidity": 30,
              }
          ),
          TemperatureSensorScenario(
              name="Bedroom",
              type="DHT11",
              state={
                  "temperature": 22,
                  "humidity": 32,
              }
          ),
      ],
      ids=generate_temperature_scenario_ids,
  )
  def test_hook_log_state__vary_gpio_and_state__logging(
      self,
      temperature_sensor_monitor_instance: TemperatureSensorMonitor,
      mocked_gpio_pins: List[mock.Mock],
      mocked_stream: StringIO,
      scenario: TemperatureSensorScenario,
  ) -> None:
    mocked_gpio_pins[0].current_state = scenario.state
    mocked_gpio_pins[0].pin_name = scenario.name
    mocked_gpio_pins[0].sensor_type = scenario.type

    temperature_sensor_monitor_instance.hook_log_state(mocked_gpio_pins[0])

    assert mocked_stream.getvalue() == (
        f"INFO - {scenario.type} - {scenario.name} - "
        f"{scenario.state['temperature']} - {scenario.state['humidity']} - "
        f"TemperatureSensor:{scenario.name}\n"
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          TemperatureSensorScenario(
              name="Kitchen",
              type="DHT11",
              state={
                  "temperature": 20,
                  "humidity": 30,
              }
          ),
          TemperatureSensorScenario(
              name="Bedroom",
              type="DHT11",
              state={
                  "temperature": 22,
                  "humidity": 32,
              }
          ),
      ],
      ids=generate_temperature_scenario_ids,
  )
  def test_hook_log_state__vary_gpio_and_state__does_not_call_slack_client(
      self,
      temperature_sensor_monitor_instance: TemperatureSensorMonitor,
      mocked_gpio_pins: List[mock.Mock],
      mocked_slack_client: mock.Mock,
      scenario: TemperatureSensorScenario,
  ) -> None:
    mocked_gpio_pins[0].current_state = scenario.state
    mocked_gpio_pins[0].pin_name = scenario.name
    mocked_gpio_pins[0].sensor_type = scenario.type

    temperature_sensor_monitor_instance.hook_log_state(mocked_gpio_pins[0])

    mocked_slack_client.return_value.send_message.assert_not_called()
