"""Test the DoorMonitor Class."""

from typing import cast
from unittest import mock

from pi_portal.modules.integrations.gpio.components import (
    contact_switch,
    door_monitor,
)
from ..bases.tests.fixtures import concrete_input, monitor_harness


class TestDoorMonitor(
    monitor_harness.GPIOMonitorTestHarness[contact_switch.ContactSwitch,
                                           door_monitor.DoorMonitor]
):
  """Test the DoorMonitor class."""

  __test__ = True
  gpio_input_1 = cast(
      contact_switch.ContactSwitch,
      concrete_input.ConcreteGPIOInput(1, "test1", 0)
  )
  gpio_input_2 = cast(
      contact_switch.ContactSwitch,
      concrete_input.ConcreteGPIOInput(2, "test2", 0)
  )

  @classmethod
  def setUpClass(cls) -> None:

    door_monitor.DoorMonitor.gpio_poll_interval = 0.01
    cls.test_class = door_monitor.DoorMonitor

  def test_hook_log_state_with_open_door(self) -> None:
    self.gpio_input_1.current_state = True
    self.gpio_input_1.pin_name = "Mock Door"

    with mock.patch.object(self.instance, "log") as m_log:
      self.instance.hook_log_state(self.gpio_input_1)

    self._slack_client().send_message.assert_called_once_with(
        f":rotating_light: The {self.gpio_input_1.pin_name} "
        f"door was OPENED!"
    )
    m_log.warning.assert_called_once_with(
        'DOOR:%s',
        self.gpio_input_1.pin_name,
        extra={
            'sensor_type': self.gpio_input_1.sensor_type,
            'sensor_name': self.gpio_input_1.pin_name,
            'state': "OPENED",
        }
    )

  def test_hook_log_state_with_close_door(self) -> None:
    self.gpio_input_1.current_state = False
    self.gpio_input_1.pin_name = "Mock Door"

    with mock.patch.object(self.instance, "log") as m_log:
      self.instance.hook_log_state(self.gpio_input_1)

    self._slack_client().send_message.assert_called_once_with(
        f":rotating_light: The {self.gpio_input_1.pin_name} "
        f"door was CLOSED!"
    )
    m_log.warning.assert_called_once_with(
        'DOOR:%s',
        self.gpio_input_1.pin_name,
        extra={
            'sensor_type': self.gpio_input_1.sensor_type,
            'sensor_name': self.gpio_input_1.pin_name,
            'state': "CLOSED",
        }
    )
