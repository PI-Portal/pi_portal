"""Tests for the TemperatureMonitorFactory class."""

from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.monitors import (
    temperature_sensor_monitor,
)
from pi_portal.modules.integrations.gpio.monitors.factories.bases import (
    monitor_factory_base,
)
from ..temperature_sensor_monitor_factory import TemperatureSensorMonitorFactory


@pytest.mark.usefixtures("test_state")
class TestTemperatureMonitorFactory:
  """Tests for the TemperatureMonitorFactory class."""

  def test_initialize__attributes(
      self,
      temp_sensor_monitor_factory_instance: TemperatureSensorMonitorFactory,
      test_state: state.State,
  ) -> None:
    assert temp_sensor_monitor_factory_instance.state.user_config == (
        test_state.user_config
    )

  def test_initialize__inheritance(
      self,
      temp_sensor_monitor_factory_instance: TemperatureSensorMonitorFactory,
  ) -> None:
    assert isinstance(
        temp_sensor_monitor_factory_instance,
        monitor_factory_base.MonitorFactoryBase,
    )

  def test_create__returns_expected_monitor(
      self,
      temp_sensor_monitor_factory_instance: TemperatureSensorMonitorFactory,
  ) -> None:
    created_instance = temp_sensor_monitor_factory_instance.create()

    assert isinstance(
        created_instance,
        temperature_sensor_monitor.TemperatureSensorMonitor,
    )

  def test_create__returns_monitor_with_expected_gpio_config(
      self,
      temp_sensor_monitor_factory_instance: TemperatureSensorMonitorFactory,
      mocked_dht11_factory_class: mock.Mock,
  ) -> None:
    created_instance = temp_sensor_monitor_factory_instance.create()

    mocked_dht11_factory_class.assert_called_once_with()
    mocked_dht11_factory_class.return_value.create.\
        assert_called_once_with()
    assert created_instance.gpio_pins == (
        mocked_dht11_factory_class.return_value.create.return_value
    )
