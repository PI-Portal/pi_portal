"""Tests for the TemperatureSensorBase class."""
from unittest import mock

import pytest
from .. import input_base, sensor_base, temperature_sensor_base
from .conftest import (
    TemperatureStateScenario,
    TypeConcreteTemperatureSensorInput,
)


class TestTemperatureSensorBase:
  """Tests for the TemperatureSensorBase class."""

  def test_initialize__attributes(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
      mocked_pin_name: str,
      mocked_pin_number: int,
  ) -> None:
    assert concrete_temperature_sensor_base_instance.pin_name == \
        mocked_pin_name
    assert concrete_temperature_sensor_base_instance.pin_number ==\
        mocked_pin_number
    assert concrete_temperature_sensor_base_instance.last_state == \
        temperature_sensor_base.EMPTY_READING
    assert concrete_temperature_sensor_base_instance.current_state == \
        temperature_sensor_base.EMPTY_READING

  def test_initialize__inheritance(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
  ) -> None:
    assert isinstance(
        concrete_temperature_sensor_base_instance,
        temperature_sensor_base.TemperatureSensorBase
    )
    assert isinstance(
        concrete_temperature_sensor_base_instance,
        sensor_base.GPIOSensorBase,
    )
    assert isinstance(
        concrete_temperature_sensor_base_instance,
        input_base.GPIOInputBase,
    )

  def test_initialize__calls_hook_setup_hardware(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
      concrete_temperature_hardware_implementation: mock.Mock,
  ) -> None:
    assert concrete_temperature_sensor_base_instance.hardware == (
        concrete_temperature_hardware_implementation
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          TemperatureStateScenario(
              current_state={
                  "temperature": 22,
                  "humidity": 32
              },
              last_state={
                  "temperature": 23,
                  "humidity": 33
              }
          ),
          TemperatureStateScenario(
              current_state={
                  "temperature": 25,
                  "humidity": 40
              },
              last_state={
                  "temperature": 26,
                  "humidity": 41
              }
          ),
      ],
  )
  def test_poll__updates_last_state__updates_current_state(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
      concrete_temperature_hardware_implementation: mock.Mock,
      scenario: TemperatureStateScenario,
  ) -> None:
    concrete_temperature_sensor_base_instance.current_state = (
        scenario.current_state
    )
    concrete_temperature_sensor_base_instance.last_state = scenario.last_state

    concrete_temperature_sensor_base_instance.poll()

    assert concrete_temperature_sensor_base_instance.last_state == (
        scenario.current_state
    )
    assert concrete_temperature_sensor_base_instance.current_state == (
        concrete_temperature_hardware_implementation.return_value
    )

  @pytest.mark.parametrize(
      "scenario,expected",
      [
          (
              TemperatureStateScenario(
                  current_state={
                      "temperature": 22,
                      "humidity": 32
                  },
                  last_state={
                      "temperature": 23,
                      "humidity": 33
                  }
              ),
              True,
          ),
          (
              TemperatureStateScenario(
                  current_state={
                      "temperature": 22,
                      "humidity": 32
                  },
                  last_state={
                      "temperature": 22,
                      "humidity": 32
                  }
              ),
              False,
          ),
      ],
  )
  def test_has_changed__updates_last_state__updates_current_state(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
      scenario: TemperatureStateScenario,
      expected: bool,
  ) -> None:
    concrete_temperature_sensor_base_instance.current_state = (
        scenario.current_state
    )
    concrete_temperature_sensor_base_instance.last_state = scenario.last_state

    result = concrete_temperature_sensor_base_instance.has_changed()

    assert result == expected

  def test_sensor_type__return_expected_value(
      self,
      concrete_temperature_sensor_base_instance:
      TypeConcreteTemperatureSensorInput,
  ) -> None:
    result = concrete_temperature_sensor_base_instance.sensor_type

    assert result == (
        concrete_temperature_sensor_base_instance.__class__.__name__
    )
