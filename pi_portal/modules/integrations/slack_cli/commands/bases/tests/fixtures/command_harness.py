"""Test harness for the CommandBase subclasses."""

import abc
from typing import Type
from unittest import TestCase, mock

from pi_portal.modules.integrations.slack_cli.commands.bases import command


class CommandBaseTestHarness(abc.ABC, TestCase):
  """Test Harness for CommandBase subclasses."""

  __test__ = False

  @abc.abstractmethod
  def get_test_class(self) -> Type[command.CommandBase]:
    """Override to return the correct test class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    self.instance = self.get_test_class()(self.mock_slack_client)
