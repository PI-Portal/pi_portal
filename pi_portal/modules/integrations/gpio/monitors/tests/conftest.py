"""Test fixtures for the GPIO monitor modules."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO
from typing import Callable, List, NamedTuple
from unittest import mock

import pytest
from ...components.bases.temperature_sensor_base import TypeTemperatureData
from .. import contact_switch_monitor, temperature_sensor_monitor


def generate_switch_scenario_ids(scenario: "ContactSwitchScenario") -> str:
  return (
      f"{scenario.name}-"
      f"{contact_switch_monitor.SwitchState(scenario.state).name}"
  )


def generate_temperature_scenario_ids(
    scenario: "TemperatureSensorScenario"
) -> str:
  return f"{scenario.name}-{scenario.state}"


class ContactSwitchScenario(NamedTuple):
  name: str
  type: str
  state: bool


class TemperatureSensorScenario(NamedTuple):
  name: str
  type: str
  state: TypeTemperatureData


@pytest.fixture
def mocked_contact_switch_logger(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(
      logging.Formatter(
          '%(levelname)s - %(sensor_type)s - %(sensor_name)s - '
          '%(state)s - %(message)s'
      )
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger


@pytest.fixture
def mocked_temperature_sensor_logger(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(
      logging.Formatter(
          '%(levelname)s - %(sensor_type)s - %(sensor_name)s - '
          '%(temperature)s - %(humidity)s - %(message)s'
      )
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger


@pytest.fixture
def contact_switch_monitor_instance(
    mocked_gpio_pins: List[mock.Mock],
    setup_monitor_mocks: Callable[[], None],
    mocked_contact_switch_logger: logging.Logger,
) -> contact_switch_monitor.ContactSwitchMonitor:
  setup_monitor_mocks()
  instance = contact_switch_monitor.ContactSwitchMonitor(mocked_gpio_pins)
  setattr(
      instance,
      "log",
      mocked_contact_switch_logger,
  )
  return instance


@pytest.fixture
def temperature_sensor_monitor_instance(
    mocked_gpio_pins: List[mock.Mock],
    setup_monitor_mocks: Callable[[], None],
    mocked_temperature_sensor_logger: logging.Logger,
) -> temperature_sensor_monitor.TemperatureSensorMonitor:
  setup_monitor_mocks()
  instance = temperature_sensor_monitor.TemperatureSensorMonitor(
      mocked_gpio_pins
  )
  setattr(
      instance,
      "log",
      mocked_temperature_sensor_logger,
  )
  return instance
