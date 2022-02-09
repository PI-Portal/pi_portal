"""Test the FileCommandBase class."""

from unittest import mock

from .fixtures import concrete_toggle_command, toggle_command_harness


class TestFileCommandBase(toggle_command_harness.ToggleCommandBaseTestHarness):
  """Test the FileCommandBase class with a concrete implementation."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = concrete_toggle_command.ConcreteToggleCommand

  @mock.patch("builtins.print")
  def test_invoke(self, m_module: mock.Mock) -> None:
    self.instance.invoke()
    m_module.assert_called_once_with("invoked ConcreteToggleCommand!")
