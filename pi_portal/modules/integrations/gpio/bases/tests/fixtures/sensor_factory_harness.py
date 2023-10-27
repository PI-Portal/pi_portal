"""Test harness for GPIO sensor factories."""

from typing import Type
from unittest import TestCase

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.bases import sensor_factory
from pi_portal.modules.integrations.gpio.components.bases import sensor


class GPIOSensorFactoryTestHarness(TestCase):
  """Test harness for GPIO sensor factories."""

  __test__ = False
  test_class: Type[sensor_factory.SensorFactoryBase]

  @mock_state.patch
  def setUp(self) -> None:
    self.factory = self.test_class()
    self.base_class = sensor_factory.SensorFactoryBase
    self.instance = self.factory.create()

  @mock_state.patch
  def test_inheritance(self) -> None:
    for created_sensor in self.instance:
      self.assertIsInstance(
          created_sensor,
          sensor.GPIOSensorBase,
      )
