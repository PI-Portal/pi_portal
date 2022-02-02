"""Test Harness for the ProcessCommandBase subclasses."""

import abc
from typing import Any, Type, Union, cast
from unittest import TestCase, mock

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    command,
    process_command,
    process_management_command,
    process_status_command,
)
from pi_portal.modules.system import supervisor_config, supervisor_process


class ProcessCommandBaseTestHarness(abc.ABC, TestCase):
  """Test Harness for the ProcessCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList

  @abc.abstractmethod
  def get_test_class(self) -> Type[process_command.ProcessCommandBase]:
    """Override to return the correct test class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    with mock.patch(command.__name__ + ".SlackNotifier") as mock_notifier:
      self.mock_notifier = mock_notifier()
      with mock.patch(
          process_command.__name__ + ".SupervisorProcess"
      ) as mock_process_class:
        self.mock_process_class = mock_process_class
        self.instance = self.get_test_class()(self.mock_slack_client)

  def _mocked_process(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.process)

  def test_instantiate(self) -> None:
    self.mock_process_class.assert_called_once_with(self.expected_process_name)

  def test_invoke(self) -> None:
    self.instance.invoke()


class ProcessExtendedCommandBaseTestHarness(abc.ABC, TestCase):
  """Test Harness for the extended ProcessCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList

  @abc.abstractmethod
  def get_test_class(
      self
  ) -> Union[Type[process_management_command.ProcessManagementCommandBase],
             Type[process_status_command.ProcessStatusCommandBase],]:
    """Override to return the correct test class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    with mock.patch(command.__name__ + ".SlackNotifier") as mock_notifier:
      self.mock_notifier = mock_notifier()
      with mock.patch(
          process_command.__name__ + ".SupervisorProcess"
      ) as mock_process_class:
        self.mock_process_class = mock_process_class
        self.instance = self.get_test_class()(self.mock_slack_client)

  def _mocked_process(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.process)

  def _mocked_process_command(self) -> Any:
    return getattr(
        self._mocked_process(),
        self.get_test_class().process_command
    )

  def _mocked_notifier(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.notifier)

  def test_instantiate(self) -> None:
    instance = self.get_test_class()(self.mock_slack_client)
    self.assertIsInstance(
        instance.process, supervisor_process.SupervisorProcess
    )
