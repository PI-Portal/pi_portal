"""Simple invoke Test Harness for the SlackProcessCommandBase subclasses."""

from typing import Type, cast
from unittest import TestCase, mock

from pi_portal.modules.integrations.slack.cli.commands.bases import (
    command,
    process_command,
)
from pi_portal.modules.system import supervisor_config


class SimpleProcessCommandBaseTestHarness(TestCase):
  """Simple invoke Test Harness for the SlackProcessCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  test_class: Type[process_command.SlackProcessCommandBase]

  def setUp(self) -> None:
    self.mock_slack_bot = mock.MagicMock()
    with mock.patch(command.__name__ + ".SlackCLINotifier") as mock_notifier:
      self.mock_notifier = mock_notifier()
      with mock.patch(
          process_command.__name__ + ".SupervisorProcess"
      ) as mock_process_class:
        self.mock_process_class = mock_process_class
        self.instance = self.test_class(self.mock_slack_bot)

  def _mocked_process(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.process)

  def test_instantiate(self) -> None:
    self.mock_process_class.assert_called_once_with(self.expected_process_name)

  def test_invoke(self) -> None:
    self.instance.invoke()
