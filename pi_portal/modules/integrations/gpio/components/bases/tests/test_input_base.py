"""Tests for the GPIOInputBase class."""
from unittest import mock

import pytest
from .. import input_base
from .conftest import IntegerStateScenario, TypeConcreteGpioInput


class TestGPIOInputBase:
  """Tests for the GPIOInputBase class."""

  def test_initialize__attributes(
      self,
      concrete_input_base_instance: TypeConcreteGpioInput,
      mocked_pin_name: str,
      mocked_pin_number: int,
      mocked_initial_state: int,
  ) -> None:
    assert concrete_input_base_instance.pin_name == mocked_pin_name
    assert concrete_input_base_instance.pin_number == mocked_pin_number
    assert concrete_input_base_instance.last_state == mocked_initial_state
    assert concrete_input_base_instance.current_state == mocked_initial_state

  def test_initialize__inheritance(
      self,
      concrete_input_base_instance: TypeConcreteGpioInput,
  ) -> None:
    assert isinstance(
        concrete_input_base_instance,
        input_base.GPIOInputBase,
    )

  @pytest.mark.usefixtures("concrete_input_base_instance")
  def test_initialize__calls_hook_setup_input(
      self,
      mocked_setup_implementation: mock.Mock,
  ) -> None:
    mocked_setup_implementation.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario",
      [
          IntegerStateScenario(current_state=2, last_state=1),
          IntegerStateScenario(current_state=5, last_state=4),
      ],
  )
  def test_poll__updates_last_state__updates_current_state(
      self,
      concrete_input_base_instance: TypeConcreteGpioInput,
      scenario: IntegerStateScenario,
  ) -> None:
    concrete_input_base_instance.current_state = scenario.current_state
    concrete_input_base_instance.last_state = scenario.last_state

    concrete_input_base_instance.poll()

    assert concrete_input_base_instance.last_state == scenario.current_state
    assert concrete_input_base_instance.current_state == (
        scenario.current_state + 1
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
      concrete_input_base_instance: TypeConcreteGpioInput,
      scenario: IntegerStateScenario,
      expected: bool,
  ) -> None:
    concrete_input_base_instance.current_state = scenario.current_state
    concrete_input_base_instance.last_state = scenario.last_state

    result = concrete_input_base_instance.has_changed()

    assert result == expected

  def test_sensor_type__return_expected_value(
      self,
      concrete_input_base_instance: TypeConcreteGpioInput,
  ) -> None:
    result = concrete_input_base_instance.sensor_type

    assert result == concrete_input_base_instance.__class__.__name__
