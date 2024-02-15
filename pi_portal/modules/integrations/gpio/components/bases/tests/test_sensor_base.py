"""Tests for the GPIOSensorBase class."""
from unittest import mock

import pytest
from .. import input_base, sensor_base
from .conftest import IntegerStateScenario, TypeConcreteSensorInput


class TestGPIOSensorBase:
  """Tests for the GPIOSensorBase class."""

  def test_initialize__attributes(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
      mocked_pin_name: str,
      mocked_pin_number: int,
      mocked_initial_state: int,
  ) -> None:
    assert concrete_sensor_base_instance.pin_name == mocked_pin_name
    assert concrete_sensor_base_instance.pin_number == mocked_pin_number
    assert concrete_sensor_base_instance.last_state == mocked_initial_state
    assert concrete_sensor_base_instance.current_state == mocked_initial_state

  def test_initialize__inheritance(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
  ) -> None:
    assert isinstance(
        concrete_sensor_base_instance,
        sensor_base.GPIOSensorBase,
    )
    assert isinstance(
        concrete_sensor_base_instance,
        input_base.GPIOInputBase,
    )

  def test_initialize__calls_hook_setup_hardware(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
      concrete_hardware_implementation: mock.Mock,
  ) -> None:
    assert concrete_sensor_base_instance.hardware == (
        concrete_hardware_implementation
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          IntegerStateScenario(current_state=2, last_state=1),
          IntegerStateScenario(current_state=5, last_state=4),
      ],
  )
  def test_poll__updates_last_state__updates_current_state(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
      concrete_hardware_implementation: mock.Mock,
      scenario: IntegerStateScenario,
  ) -> None:
    concrete_sensor_base_instance.current_state = scenario.current_state
    concrete_sensor_base_instance.last_state = scenario.last_state

    concrete_sensor_base_instance.poll()

    assert concrete_sensor_base_instance.last_state == scenario.current_state
    assert concrete_sensor_base_instance.current_state == (
        concrete_hardware_implementation.return_value
    )

  @pytest.mark.parametrize(
      "scenario,expected",
      [
          (IntegerStateScenario(current_state=2, last_state=1), True),
          (IntegerStateScenario(current_state=5, last_state=5), False),
      ],
  )
  def test_has_changed__updates_last_state__updates_current_state(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
      scenario: IntegerStateScenario,
      expected: bool,
  ) -> None:
    concrete_sensor_base_instance.current_state = scenario.current_state
    concrete_sensor_base_instance.last_state = scenario.last_state

    result = concrete_sensor_base_instance.has_changed()

    assert result == expected

  def test_sensor_type__return_expected_value(
      self,
      concrete_sensor_base_instance: TypeConcreteSensorInput,
  ) -> None:
    result = concrete_sensor_base_instance.sensor_type

    assert result == concrete_sensor_base_instance.__class__.__name__
