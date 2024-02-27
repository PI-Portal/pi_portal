"""Test the BotUptimeCommand class."""

from unittest import mock

from pi_portal.modules.system import supervisor_config
from ..bases import process_uptime_subcommand
from ..uptime_chat_bot import ChatProcessUptimeCommandBase


class TestBotUptimeCommand:
  """Test the BotUptimeCommand class."""

  def test_initialize__attributes(
      self,
      uptime_chat_bot_instance: ChatProcessUptimeCommandBase,
  ) -> None:
    assert uptime_chat_bot_instance.process_name == (
        supervisor_config.ProcessList.BOT
    )

  def test_initialize__inheritance(
      self,
      uptime_chat_bot_instance: ChatProcessUptimeCommandBase,
  ) -> None:
    assert isinstance(
        uptime_chat_bot_instance,
        process_uptime_subcommand.ChatProcessUptimeCommandBase,
    )

  def test_initialize__bot(
      self,
      uptime_chat_bot_instance: ChatProcessUptimeCommandBase,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert uptime_chat_bot_instance.chatbot == mocked_chat_bot

  def test_initialize__supervisor_process(
      self,
      uptime_chat_bot_instance: ChatProcessUptimeCommandBase,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert uptime_chat_bot_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        uptime_chat_bot_instance.process_name
    )
