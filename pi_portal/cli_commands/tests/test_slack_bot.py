"""Test the SlackBotCommand class."""

from unittest import mock

from .. import slack_bot
from ..bases import command
from ..mixins import state


class TestSlackBotCommand:
  """Test the SlackBotCommand class."""

  def test_initialize__inheritance(
      self,
      slack_bot_command_instance: slack_bot.SlackBotCommand,
  ) -> None:
    assert isinstance(slack_bot_command_instance, command.CommandBase)
    assert isinstance(
        slack_bot_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      slack_bot_command_instance: slack_bot.SlackBotCommand,
      mocked_slack_bot: mock.Mock,
  ) -> None:
    slack_bot_command_instance.invoke()

    mocked_slack_bot.assert_called_once_with()
    mocked_slack_bot.return_value.connect.assert_called_once_with()
