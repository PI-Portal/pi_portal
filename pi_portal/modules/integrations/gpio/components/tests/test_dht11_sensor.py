"""Test the DHT11 class."""

from typing import Type, cast
from unittest import mock

from pi_portal.modules.integrations.gpio.components import dht11_sensor
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from pi_portal.modules.python import rpi
from ..bases.tests.fixtures import sensor_harness


class TestGPIOInput(sensor_harness.GPIOSensorTestHarness):
  """Test the DHT11 class."""

  __test__ = True
  gpio_input_1_initial_value = temperature_sensor.EMPTY_READING
  test_class: Type[dht11_sensor.DHT11]

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = dht11_sensor.DHT11

  def _instance(self) -> dht11_sensor.DHT11:
    return cast(dht11_sensor.DHT11, self.instance)

  def _adafruit_module(self) -> mock.Mock:
    return cast(mock.Mock, rpi.adafruit_dht)

  def setUp(self) -> None:
    self._adafruit_module().reset_mock()
    self._adafruit_module().DHT11.reset_mock()
    self.instance = self.test_class(
        pin_number=self.gpio_input_1_pin,
        pin_name=self.gpio_input_1_name,
    )

  def test_hook_setup_hardware(self) -> None:
    self.assertIs(
        self._instance().hardware,
        self._adafruit_module().DHT11.return_value,
    )
    self._adafruit_module().DHT11.assert_called_once_with(
        getattr(rpi.board, f"D{self.instance.pin_number}"),
        use_pulseio=False,
    )

  def test_poll(self) -> None:
    self.instance.poll()
    self.assertDictEqual(
        {**self.instance.current_state},
        {
            "temperature": self._instance().hardware.temperature,
            "humidity": self._instance().hardware.humidity,
        },
    )

  def test_poll_with_error(self) -> None:
    with mock.patch.object(
        self.instance,
        "hardware",
    ) as m_hardware:
      type(m_hardware).temperature = mock.PropertyMock(side_effect=RuntimeError)
      self.instance.poll()
      self.assertDictEqual(
          {**self.instance.current_state},
          temperature_sensor.EMPTY_READING,
      )

  def test_sensor_type__is_expected(self) -> None:
    assert self.instance.sensor_type == "DHT11"
