"""Test fixtures for the GPIO monitor factory modules tests."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import (
    contact_switch_monitor_factory,
    temperature_sensor_monitor_factory,
)


@pytest.fixture
def mocked_contact_switches() -> List[mock.Mock]:
  return [mock.Mock()] * 3


@pytest.fixture
def mocked_contact_switch_factory_class(
    mocked_contact_switches: List[mock.Mock]
) -> mock.Mock:
  instance = mock.Mock()
  instance.return_value.create.return_value = mocked_contact_switches
  return instance


@pytest.fixture
def mocked_dht11_sensors() -> List[mock.Mock]:
  return [mock.Mock()] * 3


@pytest.fixture
def mocked_dht11_factory_class(
    mocked_dht11_sensors: List[mock.Mock]
) -> mock.Mock:
  instance = mock.Mock()
  instance.return_value.create.return_value = mocked_dht11_sensors
  return instance


@pytest.fixture
def contact_switch_monitor_factory_instance(
    mocked_contact_switch_factory_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> contact_switch_monitor_factory.ContactSwitchMonitorFactory:
  monkeypatch.setattr(
      contact_switch_monitor_factory.__name__ +
      ".contact_switch_factory.ContactSwitchFactory",
      mocked_contact_switch_factory_class,
  )
  return contact_switch_monitor_factory.ContactSwitchMonitorFactory()


@pytest.fixture(name="temp_sensor_monitor_factory_instance")
def temperature_sensor_monitor_factory_instance(
    mocked_dht11_factory_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> temperature_sensor_monitor_factory.TemperatureSensorMonitorFactory:
  monkeypatch.setattr(
      temperature_sensor_monitor_factory.__name__ +
      ".dht11_sensor_factory.DHT11Factory",
      mocked_dht11_factory_class,
  )
  return temperature_sensor_monitor_factory.TemperatureSensorMonitorFactory()
