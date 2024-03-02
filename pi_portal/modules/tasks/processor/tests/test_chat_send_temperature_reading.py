"""Test the ChatSendTemperatureReading class."""

import logging
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.chat_send_temperature_reading import (
    ProcessorClass,
)
from pi_portal.modules.tasks.processor.mixins import chat_client


@pytest.mark.usefixtures("test_state")
class TestChatSendTemperatureReading:
  """Test the ChatSendTemperatureReading class."""

  def test_initialize__attributes(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
  ) -> None:
    assert (
        chat_send_temperature_reading_instance.no_measurement_message ==
        "not yet measured"
    )
    assert (
        chat_send_temperature_reading_instance.no_sensors_configured_message ==
        "No sensors configured."
    )
    assert chat_send_temperature_reading_instance.type == \
        TaskType.CHAT_SEND_TEMPERATURE_READING

  def test_initialize__logger(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        chat_send_temperature_reading_instance.log,
        logging.Logger,
    )
    assert chat_send_temperature_reading_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        chat_send_temperature_reading_instance,
        chat_client.ChatClientMixin,
    )
    assert isinstance(
        chat_send_temperature_reading_instance,
        processor_base.TaskProcessorBase,
    )

  def test_process__no_sensors__one_type__no_results__sends_correct_message(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_chat_temperature_task: mock.Mock,
      mocked_chat_client: mock.Mock,
      mocked_temperature_log_file_reader: mock.Mock,
      test_state: state.State,
  ) -> None:
    log_file_reader = mocked_temperature_log_file_reader.return_value
    log_file_reader.read_last_values.return_value = {}
    log_file_reader.configured_sensor_count = 0
    test_state.user_config['TEMPERATURE_SENSORS'] = {"DHT11": []}

    chat_send_temperature_reading_instance.process(mocked_chat_temperature_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_temperature_task.args.header + "\n" +
        chat_send_temperature_reading_instance.no_sensors_configured_message
    )

  def test_invoke__one_sensor__one_type__no_results__sends_correct_message(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_chat_temperature_task: mock.Mock,
      mocked_chat_client: mock.Mock,
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

    chat_send_temperature_reading_instance.process(mocked_chat_temperature_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_temperature_task.args.header + "\n" + "Kitchen: " +
        chat_send_temperature_reading_instance.no_measurement_message
    )

  def test_invoke__one_sensor__one_type__results__sends_correct_message(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_chat_temperature_task: mock.Mock,
      mocked_chat_client: mock.Mock,
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

    chat_send_temperature_reading_instance.process(mocked_chat_temperature_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_temperature_task.args.header + "\n" +
        "Kitchen: 20°C, 40% humidity"
    )

  def test_invoke__two_sensors__one_type__results__sends_correct_message(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_chat_temperature_task: mock.Mock,
      mocked_chat_client: mock.Mock,
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

    chat_send_temperature_reading_instance.process(mocked_chat_temperature_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_temperature_task.args.header + "\n" +
        "Bedroom: 19°C, 39% humidity\n"
        "Kitchen: 20°C, 40% humidity"
    )

  def test_invoke__two_sensors__two_types__results__sends_correct_message(
      self,
      chat_send_temperature_reading_instance: ProcessorClass,
      mocked_chat_temperature_task: mock.Mock,
      mocked_chat_client: mock.Mock,
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

    chat_send_temperature_reading_instance.process(mocked_chat_temperature_task)

    mocked_chat_client.return_value.send_message.assert_called_once_with(
        mocked_chat_temperature_task.args.header + "\n" +
        "Kitchen: 20°C, 40% humidity\n"
        "Kitchen: 21°C, 41% humidity"
    )
