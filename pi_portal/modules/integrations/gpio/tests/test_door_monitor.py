"""Test the DoorMonitor Class."""

import logging
from typing import cast
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio import door_monitor
from pi_portal.modules.integrations.slack import client
from .fixtures.gpio_loop import patch_gpio_loop


class TestMonitorLogger(TestCase):
  """Test the DoorMonitor class."""

  @mock_state.patch
  def setUp(self) -> None:
    self.instance = door_monitor.DoorMonitor()
    self.instance.slack_client = mock.MagicMock()
    self.instance.interval = 0.01

  def _mock_slack_client(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.slack_client)

  @mock_state.patch
  def test_initialize(self) -> None:
    instance = door_monitor.DoorMonitor()
    self.assertEqual(instance.logger_name, "pi_portal")
    self.assertEqual(instance.state, config.GPIO_INITIAL_STATE)
    self.assertEqual(instance.interval, 0.5)
    self.assertEqual(instance.GPIO, door_monitor.RPi.GPIO)
    self.assertEqual(instance.GPIO_OPEN, True)
    self.assertIsInstance(instance.log, logging.Logger)
    self.assertIsInstance(instance.slack_client, client.SlackClient)

  def test_gpio_is_active(self) -> None:
    self.assertTrue(self.instance.is_running())

  @mock_state.patch
  @mock.patch("RPi.GPIO.setup")
  def test_initialize_hardware(self, m_setup: mock.Mock) -> None:
    instance = door_monitor.DoorMonitor()
    for _, pin in instance.hardware.items():
      m_setup.assert_any_call(
          pin, instance.GPIO.IN, pull_up_down=instance.GPIO.PUD_UP
      )
    self.assertEqual(m_setup.call_count, len(instance.hardware))

  @patch_gpio_loop(door_monitor.__name__ + ".DoorMonitor")
  @mock.patch(door_monitor.__name__ + ".DoorMonitor.update_state")
  def test_loop_no_change(self, m_update_state: mock.Mock) -> None:
    m_update_state.return_value = None
    mock_logger_message = "No New Messages"
    with self.assertLogs(self.instance.log, level='DEBUG') as logs:
      self.instance.log.info(mock_logger_message)
      self.instance.start()

    self.assertEqual(logs.output, [f"INFO:pi_portal:{mock_logger_message}"])
    self._mock_slack_client().\
      send_message.assert_not_called()

  @patch_gpio_loop(door_monitor.__name__ + ".DoorMonitor")
  @mock.patch(door_monitor.__name__ + ".DoorMonitor.GPIO.input")
  def test_loop_front_door_opens(self, m_input: mock.Mock) -> None:
    self.instance.state = {
        1: False,
        2: False
    }
    m_input.side_effect = [1, 0]
    with self.assertLogs(self.instance.logger_name, level='DEBUG') as logs:
      self.instance.start()

    self.assertEqual(
        logs.output, [f'WARNING:{self.instance.logger_name}:OPENED: DOOR 1']
    )
    self._mock_slack_client().send_message.assert_called_once_with(
        ':rotating_light: The front door was OPENED!'
    )

  @patch_gpio_loop(door_monitor.__name__ + ".DoorMonitor")
  @mock.patch(door_monitor.__name__ + ".DoorMonitor.GPIO.input")
  def test_loop_back_door_opens(self, m_input: mock.Mock) -> None:
    self.instance.state = {
        1: False,
        2: False
    }
    m_input.side_effect = [0, 1]
    with self.assertLogs(self.instance.logger_name, level='DEBUG') as logs:
      self.instance.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.instance.logger_name}:OPENED: DOOR 2']
    )
    self._mock_slack_client().send_message.assert_called_once_with(
        ':rotating_light: The back door was OPENED!'
    )

  @patch_gpio_loop(door_monitor.__name__ + ".DoorMonitor")
  @mock.patch(door_monitor.__name__ + ".DoorMonitor.GPIO.input")
  def test_loop_front_door_closes(self, m_input: mock.Mock) -> None:
    self.instance.state = {
        1: True,
        2: True
    }
    m_input.side_effect = [0, 1]
    with self.assertLogs(self.instance.logger_name, level='DEBUG') as logs:
      self.instance.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.instance.logger_name}:CLOSED: DOOR 1']
    )
    self._mock_slack_client().send_message.assert_called_once_with(
        ':rotating_light: The front door was CLOSED!'
    )

  @patch_gpio_loop(door_monitor.__name__ + ".DoorMonitor")
  @mock.patch(door_monitor.__name__ + ".DoorMonitor.GPIO.input")
  def test_loop_back_door_closes(self, m_input: mock.Mock) -> None:
    self.instance.state = {
        1: True,
        2: True
    }
    m_input.side_effect = [1, 0]
    with self.assertLogs(self.instance.logger_name, level='DEBUG') as logs:
      self.instance.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.instance.logger_name}:CLOSED: DOOR 2']
    )
    self._mock_slack_client().send_message.assert_called_once_with(
        ':rotating_light: The back door was CLOSED!'
    )
