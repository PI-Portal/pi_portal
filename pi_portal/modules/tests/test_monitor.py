"""Test Door Monitor Class."""

import logging
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules import monitor
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations import slack


class TestMonitorLogger(TestCase):
  """Test the Monitor class."""

  @mock_state.patch
  def setUp(self):
    self.monitor = monitor.Monitor()
    self.monitor.slack_client = mock.MagicMock()
    self.monitor.interval = 0.01

  @mock_state.patch
  def test_initialize(self):
    instance = monitor.Monitor()
    self.assertTrue(instance.running)
    self.assertEqual(instance.logger_name, "pi_portal")
    self.assertEqual(instance.state, config.GPIO_INITIAL_STATE)
    self.assertEqual(instance.interval, 0.5)
    self.assertEqual(instance.GPIO, monitor.RPi.GPIO)
    self.assertEqual(instance.GPIO_OPEN, True)
    self.assertIsInstance(instance.log, logging.Logger)
    self.assertIsInstance(instance.slack_client, slack.Client)

  @mock_state.patch
  @mock.patch("RPi.GPIO.setup")
  def test_initialize_hardware(self, m_setup):
    instance = monitor.Monitor()
    for _, pin in instance.hardware.items():
      m_setup.assert_any_call(
          pin, instance.GPIO.IN, pull_up_down=instance.GPIO.PUD_UP
      )
    self.assertEqual(m_setup.call_count, len(instance.hardware))

  @mock.patch(
      monitor.__name__ + ".Monitor.running", new_callable=mock.PropertyMock
  )
  @mock.patch(monitor.__name__ + ".Monitor.update_state")
  def test_loop_no_change(self, m_update_state, m_running):
    m_running.side_effect = [True, False]
    m_update_state.return_value = None
    mock_logger_message = "No New Messages"
    with self.assertLogs(self.monitor.log, level='DEBUG') as logs:
      self.monitor.log.info(mock_logger_message)
      self.monitor.start()
    self.assertEqual(logs.output, [f"INFO:pi_portal:{mock_logger_message}"])
    self.monitor.slack_client.send_message.assert_not_called()

  @mock.patch(
      monitor.__name__ + ".Monitor.running", new_callable=mock.PropertyMock
  )
  @mock.patch(monitor.__name__ + ".Monitor.GPIO.input")
  def test_loop_front_door_opens(self, m_input, m_running):
    self.monitor.state = {
        1: False,
        2: False
    }
    m_running.side_effect = [True, False]
    m_input.side_effect = [1, 0]
    with self.assertLogs(self.monitor.logger_name, level='DEBUG') as logs:
      self.monitor.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.monitor.logger_name}:OPENED: DOOR 1']
    )
    self.monitor.slack_client.send_message.assert_called_once_with(
        ':rotating_light: The front door was OPENED!'
    )

  @mock.patch(
      monitor.__name__ + ".Monitor.running", new_callable=mock.PropertyMock
  )
  @mock.patch(monitor.__name__ + ".Monitor.GPIO.input")
  def test_loop_back_door_opens(self, m_input, m_running):
    self.monitor.state = {
        1: False,
        2: False
    }
    m_running.side_effect = [True, False]
    m_input.side_effect = [0, 1]
    with self.assertLogs(self.monitor.logger_name, level='DEBUG') as logs:
      self.monitor.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.monitor.logger_name}:OPENED: DOOR 2']
    )
    self.monitor.slack_client.send_message.assert_called_once_with(
        ':rotating_light: The back door was OPENED!'
    )

  @mock.patch(
      monitor.__name__ + ".Monitor.running", new_callable=mock.PropertyMock
  )
  @mock.patch(monitor.__name__ + ".Monitor.GPIO.input")
  def test_loop_front_door_closes(self, m_input, m_running):
    self.monitor.state = {
        1: True,
        2: True
    }
    m_running.side_effect = [True, False]
    m_input.side_effect = [0, 1]
    with self.assertLogs(self.monitor.logger_name, level='DEBUG') as logs:
      self.monitor.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.monitor.logger_name}:CLOSED: DOOR 1']
    )
    self.monitor.slack_client.send_message.assert_called_once_with(
        ':rotating_light: The front door was CLOSED!'
    )

  @mock.patch(
      monitor.__name__ + ".Monitor.running", new_callable=mock.PropertyMock
  )
  @mock.patch(monitor.__name__ + ".Monitor.GPIO.input")
  def test_loop_back_door_closes(self, m_input, m_running):
    self.monitor.state = {
        1: True,
        2: True
    }
    m_running.side_effect = [True, False]
    m_input.side_effect = [1, 0]
    with self.assertLogs(self.monitor.logger_name, level='DEBUG') as logs:
      self.monitor.start()
    self.assertEqual(
        logs.output, [f'WARNING:{self.monitor.logger_name}:CLOSED: DOOR 2']
    )
    self.monitor.slack_client.send_message.assert_called_once_with(
        ':rotating_light: The back door was CLOSED!'
    )
