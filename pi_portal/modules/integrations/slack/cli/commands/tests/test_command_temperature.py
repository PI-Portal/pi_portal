"""Test the TemperatureCommand class."""

from unittest import mock

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from pi_portal.modules.integrations.slack.cli.commands import TemperatureCommand
from ..bases import command


class TestTemperatureCommand:
  """Test the TemperatureCommand class."""

  def test_initialize__inheritance(
      self,
      temperature_command_instance: TemperatureCommand,
  ) -> None:
    assert isinstance(
        temperature_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__no_sensors__one_type__no_results__sends_correct_message(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
      mocked_state: state.State,
      mocked_temperature_log_file_reader: mock.Mock,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.read_last_values.return_value = {}
    log_file_reader.configured_sensor_count = 0
    mocked_state.user_config['TEMPERATURE_SENSORS'] = {"DHT11": []}

    temperature_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "No sensors configured."
    )

  def test_invoke__one_sensor__one_type__no_results__sends_correct_message(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
      mocked_temperature_log_file_reader: mock.Mock,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.configured_sensor_count = 1
    log_file_reader.read_last_values.return_value = {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=None,
                        temperature=None,
                    )
            }
    }

    temperature_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "Kitchen: not yet measured"
    )

  def test_invoke__one_sensor__one_type__results__sends_correct_message(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
      mocked_temperature_log_file_reader: mock.Mock,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.configured_sensor_count = 1
    log_file_reader.read_last_values.return_value = {
        "DHT11":
            {
                "Kitchen":
                    temperature_sensor_base.TypeTemperatureData(
                        humidity=40,
                        temperature=20,
                    )
            }
    }

    temperature_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "Kitchen: 20°C, 40% humidity"
    )

  def test_invoke__two_sensors__one_type__results__sends_correct_message(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
      mocked_temperature_log_file_reader: mock.Mock,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.configured_sensor_count = 2
    log_file_reader.read_last_values.return_value = {
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

    temperature_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        ("Bedroom: 19°C, 39% humidity\n"
         "Kitchen: 20°C, 40% humidity")
    )

  def test_invoke__two_sensors__two_types__results__sends_correct_message(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
      mocked_temperature_log_file_reader: mock.Mock,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.configured_sensor_count = 2
    log_file_reader.read_last_values.return_value = {
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

    temperature_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        ("Kitchen: 20°C, 40% humidity\n"
         "Kitchen: 21°C, 41% humidity")
    )
