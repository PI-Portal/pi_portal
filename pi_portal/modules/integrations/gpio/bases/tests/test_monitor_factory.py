"""Test the GPIO factory base classes."""

from unittest import TestCase

from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from ...components.bases.tests.fixtures import concrete_monitor
from .. import monitor_factory


class ConcreteMonitorFactory(
    monitor_factory.MonitorFactoryBase[gpio_input.GPIOInputBase]
):
  """Concrete implementation of the MonitorFactoryBase class."""

  def create(self) -> concrete_monitor.ConcreteGPIOMonitor:
    """Override with creation logic."""

    return concrete_monitor.ConcreteGPIOMonitor([])


class TestMonitorFactoryBase(TestCase):
  """Test the MonitorFactoryBase class with a concrete implementation."""

  @mock_state.patch
  def setUp(self) -> None:
    self.factory = ConcreteMonitorFactory()

  def test_instantiation(self) -> None:
    factory = ConcreteMonitorFactory()
    self.assertIsInstance(
        factory.state,
        state.State,
    )

  @mock_state.patch
  def test_create(self) -> None:
    instance = self.factory.create()
    self.assertIsInstance(instance, concrete_monitor.ConcreteGPIOMonitor)
    self.assertEqual(
        len(instance.gpio_pins),
        0,
    )
