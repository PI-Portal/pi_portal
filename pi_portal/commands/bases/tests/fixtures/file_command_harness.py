"""CLI FileCommandBase test harness."""

import abc
from typing import Type
from unittest import TestCase, mock

from ... import file_command


class FileCommandBaseTestHarness(TestCase, abc.ABC):
  """CLI FileCommandBase test harness."""

  __test__ = False
  test_class: Type[file_command.FileCommandBase]

  def setUp(self) -> None:
    self.mock_file = "mock_file"
    self.instance = self.test_class(self.mock_file)

  def test_instantiate(self) -> None:
    self.assertEqual(
        self.mock_file,
        self.instance.file_name,
    )

  @abc.abstractmethod
  def test_invoke(self, m_module: mock.Mock) -> None:
    """Override to test the invoke class."""
