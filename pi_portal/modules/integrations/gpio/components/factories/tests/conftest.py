"""Test fixtures for the GPIO component factories."""

from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from .. import contact_switch_factory, dht11_sensor_factory


@pytest.fixture
def contact_switch_factory_instance(
    mocked_state: mock.Mock,
) -> contact_switch_factory.ContactSwitchFactory:
  state.State().user_config = mocked_state.user_config
  return contact_switch_factory.ContactSwitchFactory()


@pytest.fixture
def dht11_factory_instance(
    mocked_state: mock.Mock,
) -> dht11_sensor_factory.DHT11Factory:
  state.State().user_config = mocked_state.user_config
  return dht11_sensor_factory.DHT11Factory()
