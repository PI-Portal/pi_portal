"""CLI ToggleCommandBase test harness."""

import abc
from typing import Type
from unittest import TestCase, mock

from ... import toggle_command


class ToggleCommandBaseTestHarness(TestCase, abc.ABC):
  """CLI ToggleCommandBase test harness."""

  __test__ = False
  test_class: Type[toggle_command.ToggleCommandBase]

  def setUp(self) -> None:
    self.mock_toggle = True
    self.instance = self.test_class(self.mock_toggle)

  def test_instantiate(self) -> None:
    self.assertEqual(
        self.mock_toggle,
        self.instance.toggle,
    )

  @abc.abstractmethod
  def test_invoke(self, m_module: mock.Mock) -> None:
    """Override to test the invoke class."""
