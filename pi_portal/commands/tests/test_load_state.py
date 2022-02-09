"""Test the LoadStateCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import toggle_command_harness
from .. import load_state


class TestLoadStateCommand(toggle_command_harness.ToggleCommandBaseTestHarness):
  """Test the LoadStateCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = load_state.LoadStateCommand

  @mock.patch(load_state.__name__ + ".state")
  def test_invoke(self, m_module: mock.Mock) -> None:
    self.instance.invoke()
    m_module.State.assert_called_once_with()
    m_module.State.return_value.load.assert_called_once_with()
