"""Test the DoorMonitorFactory class."""

from unittest import TestCase

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.components import door_monitor
from ..door_monitor_factory import DoorMonitorFactory


class TestDoorMonitorFactory(TestCase):
  """Test the DoorMonitorFactory class."""

  @mock_state.patch
  def setUp(self) -> None:
    self.factory = DoorMonitorFactory()

  @mock_state.patch
  def test_create(self) -> None:
    instance = self.factory.create()
    self.assertIsInstance(
        instance,
        door_monitor.DoorMonitor,
    )
    self.assertEqual(
        len(instance.gpio_pins),
        1,
    )
    self.assertEqual(
        instance.gpio_pins[0].pin_name,
        self.factory.state.user_config['CONTACT_SWITCHES'][0]["NAME"]
    )
    self.assertEqual(
        instance.gpio_pins[0].pin_number,
        self.factory.state.user_config['CONTACT_SWITCHES'][0]["GPIO"]
    )
