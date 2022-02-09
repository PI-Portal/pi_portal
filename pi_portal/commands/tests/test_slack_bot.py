"""Test the SlackBotCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import command_harness
from .. import slack_bot
from ..mixins import state


class TestSlackBotCommand(command_harness.CommandBaseTestHarness):
  """Test the SlackBotCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = slack_bot.SlackBotCommand

  def test_mixins(self) -> None:
    self.assertIsInstance(self.instance, state.CommandManagedStateMixin)

  @mock.patch(slack_bot.__name__ + ".slack")
  def test_invoke(self, m_module: mock.Mock) -> None:

    self.instance.invoke()
    m_module.SlackBot.assert_called_once_with()
    m_module.SlackBot.return_value.connect.assert_called_once_with()
