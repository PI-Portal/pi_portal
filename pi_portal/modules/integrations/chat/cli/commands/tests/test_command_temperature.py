"""Test the TemperatureCommand class."""

from unittest import mock

from pi_portal.modules.integrations.chat.cli.commands import TemperatureCommand
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

  def test_invoke__calls_chat_send_temperature_reading(
      self,
      temperature_command_instance: TemperatureCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    temperature_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client.\
        chat_send_temperature_reading.assert_called_once_with()
