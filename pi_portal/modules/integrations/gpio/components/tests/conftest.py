"""Test fixtures for the GPIO component module tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import contact_switch, dht11_sensor


@pytest.fixture
def mocked_humidity_property() -> mock.PropertyMock:
  return mock.PropertyMock()


@pytest.fixture
def mocked_pin_name() -> str:
  return "mock_pin_name"


@pytest.fixture
def mocked_pin_number() -> int:
  return 9


@pytest.fixture
def mocked_rpi_dht_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_rpi_dht_module_with_dht11(
    mocked_rpi_dht_module: mock.Mock,
    mocked_humidity_property: mock.PropertyMock,
    mocked_temperature_property: mock.PropertyMock,
) -> mock.Mock:
  type(mocked_rpi_dht_module.DHT11.return_value).temperature = \
      mocked_temperature_property
  type(mocked_rpi_dht_module.DHT11.return_value).humidity = \
      mocked_humidity_property
  return mocked_rpi_dht_module


@pytest.fixture
def mocked_rpi_board_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_rpi_gpio_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_temperature_property() -> mock.PropertyMock:
  return mock.PropertyMock()


@pytest.fixture
def contact_switch_instance(
    mocked_rpi_gpio_module: mock.Mock,
    mocked_pin_name: str,
    mocked_pin_number: int,
    monkeypatch: pytest.MonkeyPatch,
) -> contact_switch.ContactSwitch:
  monkeypatch.setattr(
      contact_switch.__name__ + ".RPi.GPIO",
      mocked_rpi_gpio_module,
  )
  return contact_switch.ContactSwitch(
      pin_number=mocked_pin_number,
      pin_name=mocked_pin_name,
  )


@pytest.fixture
def dht11_sensor_sensor_instance(
    mocked_rpi_dht_module_with_dht11: mock.Mock,
    mocked_rpi_board_module: mock.Mock,
    mocked_pin_name: str,
    mocked_pin_number: int,
    monkeypatch: pytest.MonkeyPatch,
) -> dht11_sensor.DHT11:
  monkeypatch.setattr(
      dht11_sensor.__name__ + ".adafruit_dht",
      mocked_rpi_dht_module_with_dht11,
  )
  monkeypatch.setattr(
      dht11_sensor.__name__ + ".board",
      mocked_rpi_board_module,
  )
  return dht11_sensor.DHT11(
      pin_number=mocked_pin_number,
      pin_name=mocked_pin_name,
  )
