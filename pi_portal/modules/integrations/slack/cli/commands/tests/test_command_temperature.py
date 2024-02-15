"""Test the Slack CLI Temperature Command."""

from unittest import mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from pi_portal.modules.integrations.log_file import temperature_monitor_logfile
from pi_portal.modules.integrations.slack.cli.commands import (
    command_temperature,
)
from ..bases.tests.fixtures import command_harness

TEMPERATURE_MONITOR_LOGFILE = temperature_monitor_logfile.__name__


class TestStatusCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Status Command."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_temperature.TemperatureCommand

  @mock.patch(TEMPERATURE_MONITOR_LOGFILE + ".TemperatureMonitorLogFileReader")
  def test_invoke__no_sensors__no_results(self, m_log: mock.Mock) -> None:
    m_log.return_value.read_last_values.return_value = {}
    m_log.return_value.configured_sensor_count = 0
    with mock_state.mock_state_creator() as mocked_state:
      mocked_state.user_config['TEMPERATURE_SENSORS'] = {}

      self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        "No sensors configured."
    )

  @mock_state.patch
  @mock.patch(TEMPERATURE_MONITOR_LOGFILE + ".TemperatureMonitorLogFileReader")
  def test_invoke__one_sensor__no_results(self, m_log: mock.Mock) -> None:
    m_log.return_value.configured_sensor_count = 1
    m_log.return_value.read_last_values.return_value = {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=None,
                        temperature=None,
                    )
            }
    }

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        "Kitchen: not yet measured"
    )

  @mock_state.patch
  @mock.patch(TEMPERATURE_MONITOR_LOGFILE + ".TemperatureMonitorLogFileReader")
  def test_invoke__one_sensor__results(self, m_log: mock.Mock) -> None:
    m_log.return_value.configured_sensor_count = 1
    m_log.return_value.read_last_values.return_value = {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=40,
                        temperature=20,
                    )
            }
    }

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        "Kitchen: 20°C, 40% humidity"
    )

  @mock_state.patch
  @mock.patch(TEMPERATURE_MONITOR_LOGFILE + ".TemperatureMonitorLogFileReader")
  def test_invoke__two_sensors__results(self, m_log: mock.Mock) -> None:
    m_log.return_value.configured_sensor_count = 2
    m_log.return_value.read_last_values.return_value = {
        "DHT11":
            {
                "Bedroom":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=39,
                        temperature=19,
                    ),
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=40,
                        temperature=20,
                    )
            }
    }

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        ("Bedroom: 19°C, 39% humidity\n"
         "Kitchen: 20°C, 40% humidity")
    )

  @mock_state.patch
  @mock.patch(TEMPERATURE_MONITOR_LOGFILE + ".TemperatureMonitorLogFileReader")
  def test_invoke__two_sensor_types__results(self, m_log: mock.Mock) -> None:
    m_log.return_value.configured_sensor_count = 2
    m_log.return_value.read_last_values.return_value = {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=40,
                        temperature=20,
                    )
            },
        "UNKNOWN":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=41,
                        temperature=21,
                    )
            }
    }

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        ("Kitchen: 20°C, 40% humidity\n"
         "Kitchen: 21°C, 41% humidity")
    )
