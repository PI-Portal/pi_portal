"""Test harness for GPIO monitor factories."""

import abc
from typing import Type
from unittest import TestCase

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.bases import factory
from pi_portal.modules.integrations.gpio.components.bases import monitor


class GPIOMonitorFactoryTestHarness(TestCase):
  """Test harness for GPIO monitor factories."""

  __test__ = False
  test_class: Type[factory.MonitorFactoryBase]
  gpio_input_type: Type[monitor.GPIOMonitorBase]

  @mock_state.patch
  def setUp(self) -> None:
    self.factory = self.test_class()
    self.instance = self.factory.create()

  @mock_state.patch
  def test_create(self) -> None:
    self.assertIsInstance(
        self.instance,
        self.gpio_input_type,
    )
    self.assertEqual(
        len(self.instance.gpio_pins),
        1,
    )

  @abc.abstractmethod
  def test_gpio(self) -> None:
    """Override to test the GPIO pins in the generated instance."""
