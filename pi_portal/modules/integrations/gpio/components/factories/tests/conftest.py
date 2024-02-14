"""Test fixtures for the GPIO component factories."""

import pytest
from .. import contact_switch_factory, dht11_sensor_factory


@pytest.fixture
def contact_switch_factory_instance(
) -> contact_switch_factory.ContactSwitchFactory:
  return contact_switch_factory.ContactSwitchFactory()


@pytest.fixture
def dht11_factory_instance() -> dht11_sensor_factory.DHT11Factory:
  return dht11_sensor_factory.DHT11Factory()
