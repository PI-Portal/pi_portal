"""Test fixtures for the GPIO component base classes."""
# pylint: disable=redefined-outer-name

from typing import NamedTuple, Type, cast
from unittest import mock

import pytest
from .. import input_base, sensor_base, temperature_sensor_base

TypeConcreteGpioInput = input_base.GPIOInputBase[int]
TypeConcreteSensorInput = sensor_base.GPIOSensorBase[int, mock.Mock]
TypeConcreteTemperatureSensorInput = (
    temperature_sensor_base.TemperatureSensorBase[
        sensor_base.TypeGenericHardware]
)


class IntegerStateScenario(NamedTuple):
  current_state: int
  last_state: int


class TemperatureStateScenario(NamedTuple):
  current_state: temperature_sensor_base.TypeTemperatureData
  last_state: temperature_sensor_base.TypeTemperatureData


@pytest.fixture
def mocked_initial_state() -> int:
  return 0


@pytest.fixture
def mocked_pin_name() -> str:
  return "mock_pin_name"


@pytest.fixture
def mocked_pin_number() -> int:
  return 9


@pytest.fixture
def mocked_setup_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_hardware_implementation() -> mock.Mock:
  return mock.Mock(return_value=1001)


@pytest.fixture
def concrete_input_base_class(
    mocked_setup_implementation: mock.Mock,
) -> Type[TypeConcreteGpioInput]:

  class ConcreteGPIOInput(input_base.GPIOInputBase[int]):

    def hook_setup_input(self) -> None:
      mocked_setup_implementation()

    def hook_update_state(self) -> int:
      return self.last_state + 1

  return ConcreteGPIOInput


@pytest.fixture
def concrete_input_base_instance(
    concrete_input_base_class: Type[TypeConcreteGpioInput],
    mocked_pin_name: str,
    mocked_pin_number: int,
    mocked_initial_state: int,
) -> TypeConcreteGpioInput:
  return concrete_input_base_class(
      pin_number=mocked_pin_number,
      pin_name=mocked_pin_name,
      initial_state=mocked_initial_state,
  )


@pytest.fixture
def concrete_sensor_base_class(
    concrete_hardware_implementation: mock.Mock,
) -> Type[TypeConcreteSensorInput]:

  class ConcreteGPIOSensor(sensor_base.GPIOSensorBase[int, mock.Mock]):

    def hook_setup_hardware(self) -> mock.Mock:
      return concrete_hardware_implementation

    def hook_update_state(self) -> int:
      return cast(int, self.hardware())

  return ConcreteGPIOSensor


@pytest.fixture
def concrete_sensor_base_instance(
    concrete_sensor_base_class: Type[TypeConcreteSensorInput],
    mocked_pin_name: str,
    mocked_pin_number: int,
    mocked_initial_state: int,
) -> TypeConcreteSensorInput:
  return concrete_sensor_base_class(
      pin_number=mocked_pin_number,
      pin_name=mocked_pin_name,
      initial_state=mocked_initial_state,
  )


@pytest.fixture
def concrete_temperature_hardware_implementation() -> mock.Mock:
  return mock.Mock(
      return_value=temperature_sensor_base.TypeTemperatureData(
          temperature=23, humidity=33
      ),
  )


@pytest.fixture
def concrete_temperature_sensor_base_class(
    concrete_temperature_hardware_implementation: mock.Mock,
) -> Type[TypeConcreteTemperatureSensorInput]:

  class ConcreteGPIOTemperatureSensor(
      temperature_sensor_base.TemperatureSensorBase[mock.Mock]
  ):

    def hook_setup_hardware(self) -> mock.Mock:
      return concrete_temperature_hardware_implementation

    def hook_update_state(self) -> temperature_sensor_base.TypeTemperatureData:
      return cast(temperature_sensor_base.TypeTemperatureData, self.hardware())

  return ConcreteGPIOTemperatureSensor


@pytest.fixture
def concrete_temperature_sensor_base_instance(
    concrete_temperature_sensor_base_class: Type[mock.Mock],
    mocked_pin_name: str,
    mocked_pin_number: int,
) -> TypeConcreteSensorInput:
  return concrete_temperature_sensor_base_class(
      pin_number=mocked_pin_number,
      pin_name=mocked_pin_name,
  )
