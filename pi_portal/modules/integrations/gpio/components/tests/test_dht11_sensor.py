"""Test the DHT11 class."""

from unittest import mock

from .. import dht11_sensor
from ..bases.temperature_sensor_base import EMPTY_READING, TemperatureSensorBase


class TestDHT11:
  """Test the DHT11 class."""

  def test_initialize__attributes(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_pin_name: str,
      mocked_pin_number: int,
  ) -> None:
    assert dht11_sensor_sensor_instance.pin_name == mocked_pin_name
    assert dht11_sensor_sensor_instance.pin_number == mocked_pin_number
    assert dht11_sensor_sensor_instance.last_state == EMPTY_READING
    assert dht11_sensor_sensor_instance.current_state == EMPTY_READING

  def test_initialize__inheritance(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
  ) -> None:
    assert isinstance(
        dht11_sensor_sensor_instance,
        TemperatureSensorBase,
    )

  def test_initialize__hardware_setup(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_rpi_dht_module: mock.Mock,
      mocked_rpi_board_module: mock.Mock,
  ) -> None:
    mocked_board_pin = getattr(
        mocked_rpi_board_module,
        f"D{dht11_sensor_sensor_instance.pin_number}",
    )
    assert dht11_sensor_sensor_instance.hardware == (
        mocked_rpi_dht_module.DHT11.return_value
    )
    mocked_rpi_dht_module.DHT11.assert_called_once_with(
        mocked_board_pin,
        use_pulseio=False,
    )

  def test_hook_update_state__nominal_reading__correct_data(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_humidity_property: mock.PropertyMock,
      mocked_temperature_property: mock.PropertyMock,
  ) -> None:
    mocked_humidity_property.return_value = 30
    mocked_temperature_property.return_value = 20

    return_value = dht11_sensor_sensor_instance.hook_update_state()

    assert return_value["temperature"] == 20
    assert return_value["humidity"] == 30
    assert mocked_temperature_property.call_count == 1
    assert mocked_humidity_property.call_count == 1

  def test_hook_update_state__1_error_reading__correct_new_reading(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_humidity_property: mock.PropertyMock,
      mocked_temperature_property: mock.PropertyMock,
  ) -> None:
    mocked_humidity_property.side_effect = [30]
    mocked_temperature_property.side_effect = [RuntimeError, 20]

    return_value = dht11_sensor_sensor_instance.hook_update_state()

    assert return_value["temperature"] == 20
    assert return_value["humidity"] == 30
    assert mocked_temperature_property.call_count == 2
    assert mocked_humidity_property.call_count == 1

  def test_hook_update_state__2_error_readings__correct_new_reading(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_humidity_property: mock.PropertyMock,
      mocked_temperature_property: mock.PropertyMock,
  ) -> None:
    mocked_humidity_property.side_effect = [RuntimeError, 30]
    mocked_temperature_property.side_effect = [RuntimeError, 20, 20]

    return_value = dht11_sensor_sensor_instance.hook_update_state()

    assert return_value["temperature"] == 20
    assert return_value["humidity"] == 30
    assert mocked_temperature_property.call_count == 3
    assert mocked_humidity_property.call_count == 2

  def test_hook_update_state__3_error_readings__returns_current_state(
      self,
      dht11_sensor_sensor_instance: dht11_sensor.DHT11,
      mocked_temperature_property: mock.PropertyMock,
  ) -> None:
    mocked_temperature_property.side_effect = [
        RuntimeError, RuntimeError, RuntimeError
    ]
    assert dht11_sensor_sensor_instance.current_state == EMPTY_READING

    return_value = dht11_sensor_sensor_instance.hook_update_state()

    assert return_value == EMPTY_READING
