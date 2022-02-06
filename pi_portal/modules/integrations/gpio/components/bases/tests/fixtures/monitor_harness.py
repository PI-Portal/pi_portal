"""GPIO monitor test harness."""

import abc
import logging
from typing import Type, cast
from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.components.bases import monitor
from pi_portal.modules.integrations.slack import client
from ... import input as gpio_input
from . import gpio_loop


@mock.patch(monitor.__name__ + ".RPi.GPIO")
class GPIOMonitorTestHarness(TestCase, abc.ABC):
  """Test harness for the GPIOMonitorBase class."""

  __test__ = False
  gpio_input_1: gpio_input.GPIOInputBase
  gpio_input_2: gpio_input.GPIOInputBase
  test_class: Type[monitor.GPIOMonitorBase]

  @mock_state.patch
  def setUp(self) -> None:
    super().setUp()
    self.instance = self.test_class([self.gpio_input_1, self.gpio_input_2])
    self.instance.slack_client = mock.Mock()
    self.instance.log.handlers = [logging.StreamHandler()]

  def _slack_client(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.slack_client)

  @mock_state.patch
  def test_initialize(self, m_rpio: mock.Mock) -> None:
    instance = self.test_class([self.gpio_input_1, self.gpio_input_2])
    self.assertIsInstance(instance.log, logging.Logger)
    self.assertIsInstance(instance.slack_client, client.SlackClient)
    self.assertEqual(instance.gpio_pins, [self.gpio_input_1, self.gpio_input_2])
    m_rpio.setmode.assert_called_once_with(m_rpio.BCM)
    m_rpio.setup.assert_any_call(
        self.gpio_input_1.pin_number, m_rpio.IN, pull_up_down=m_rpio.PUD_UP
    )
    m_rpio.setup.assert_any_call(
        self.gpio_input_2.pin_number, m_rpio.IN, pull_up_down=m_rpio.PUD_UP
    )
    self.assertEqual(m_rpio.setup.call_count, 2)

  def test_is_running(self, _: mock.Mock) -> None:
    self.assertTrue(self.instance.is_running())

  @gpio_loop.patch_gpio_loop(monitor.__name__ + ".GPIOMonitorBase")
  def test_pins_are_polled(self, _: mock.Mock) -> None:
    with mock.patch.object(self.instance.gpio_pins[0], "poll") as m_poll_1:
      with mock.patch.object(self.instance.gpio_pins[1], "poll") as m_poll_2:
        self.instance.start()
        m_poll_1.assert_called_once_with()
        m_poll_2.assert_called_once_with()
