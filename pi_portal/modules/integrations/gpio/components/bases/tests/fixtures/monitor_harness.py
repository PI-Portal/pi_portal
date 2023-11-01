"""GPIO monitor test harness."""

import abc
import logging
from typing import Any, Generic, Type, TypeVar, cast
from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.components.bases import monitor
from pi_portal.modules.integrations.gpio.components.bases.monitor import (
    TypeGenericGpio,
)
from pi_portal.modules.integrations.slack import client
from . import gpio_loop

TypeGPIOMonitorSubClass = TypeVar(
    'TypeGPIOMonitorSubClass', bound=monitor.GPIOMonitorBase[Any]
)


class GPIOMonitorTestHarness(
    TestCase, abc.ABC, Generic[TypeGenericGpio, TypeGPIOMonitorSubClass]
):
  """Test harness for the GPIOMonitorBase class."""

  __test__ = False
  gpio_input_1: TypeGenericGpio
  gpio_input_2: TypeGenericGpio
  test_class: Type[TypeGPIOMonitorSubClass]

  @mock_state.patch
  def setUp(self) -> None:
    super().setUp()
    self.instance = self.test_class([self.gpio_input_1, self.gpio_input_2])
    self.instance.slack_client = mock.Mock()
    self.instance.log.handlers = [logging.StreamHandler()]

  def _slack_client(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.slack_client)

  @mock_state.patch
  def test_initialize(self) -> None:
    instance = self.test_class([self.gpio_input_1, self.gpio_input_2])
    self.assertIsInstance(instance.log, logging.Logger)
    self.assertIsInstance(instance.slack_client, client.SlackClient)
    self.assertEqual(instance.gpio_pins, [self.gpio_input_1, self.gpio_input_2])

  @mock_state.patch
  def test_initialize_gpio(self) -> None:
    with mock.patch(monitor.__name__ + ".RPi") as m_rpi:
      self.test_class([self.gpio_input_1, self.gpio_input_2])
    m_rpi.GPIO.setmode.assert_called_once_with(m_rpi.GPIO.BCM)

  def test_is_running(self) -> None:
    self.assertTrue(self.instance.is_running())

  @gpio_loop.patch_gpio_loop(monitor.__name__ + ".GPIOMonitorBase")
  def test_pins_are_polled(self) -> None:
    with mock.patch.object(self.instance, "hook_log_state"):
      with mock.patch.object(self.instance.gpio_pins[0], "poll") as m_poll_1:
        with mock.patch.object(self.instance.gpio_pins[1], "poll") as m_poll_2:
          self.instance.start()
          m_poll_1.assert_called_once_with()
          m_poll_2.assert_called_once_with()
