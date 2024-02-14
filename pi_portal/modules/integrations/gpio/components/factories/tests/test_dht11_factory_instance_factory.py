"""Test the TemperatureSensorFactory class."""

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components import dht11_sensor
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from ..bases import (
    input_factory_base,
    sensor_factory_base,
    temperature_factory_base,
)
from ..dht11_sensor_factory import DHT11Factory


@pytest.mark.usefixtures("test_state")
class TestTemperatureSensorFactory:
  """Test the TemperatureSensorFactory class."""

  def test_initiate__attributes(
      self,
      dht11_factory_instance: DHT11Factory,
      test_state: state.State,
  ) -> None:
    assert isinstance(
        dht11_factory_instance.state,
        state.State,
    )
    assert dht11_factory_instance.state.user_config == test_state.user_config

  def test_initiate__inheritance(
      self,
      dht11_factory_instance: DHT11Factory,
  ) -> None:
    assert isinstance(
        dht11_factory_instance,
        temperature_factory_base.TemperatureSensorFactoryBase,
    )
    assert isinstance(
        dht11_factory_instance,
        sensor_factory_base.SensorFactoryBase,
    )
    assert isinstance(
        dht11_factory_instance,
        input_factory_base.GPIOInputFactoryBase,
    )

  def test_create__returns_sensors(
      self,
      dht11_factory_instance: DHT11Factory,
  ) -> None:
    result = dht11_factory_instance.create()

    for sensor in result:
      assert isinstance(
          sensor,
          temperature_sensor_base.TemperatureSensorBase,
      )

  def test_create__returns_correctly_configured_sensors(
      self,
      dht11_factory_instance: DHT11Factory,
      test_state: state.State,
  ) -> None:
    result = dht11_factory_instance.create()

    for index, configured_dht11_sensor in enumerate(
        test_state.user_config["TEMPERATURE_SENSORS"]["DHT11"]
    ):
      assert result[index].sensor_type == dht11_sensor.DHT11.__name__
      assert result[index].pin_name == configured_dht11_sensor["NAME"]
      assert result[index].pin_number == configured_dht11_sensor["GPIO"]
