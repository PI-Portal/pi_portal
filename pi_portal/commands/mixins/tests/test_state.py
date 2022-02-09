"""Test the CommandManagedStateMixin class."""

import logging
from unittest import TestCase, mock

from .. import state


class TestLoadStateCommand(TestCase):
  """Test the CommandManagedStateMixin class."""

  def setUp(self) -> None:
    self.instance = state.CommandManagedStateMixin()

  @mock.patch(state.__name__ + ".state")
  def test_load_state(self, m_state: mock.Mock) -> None:
    self.instance.load_state(False)
    m_state.State.assert_called_once_with()
    m_state.State.return_value.load.assert_called_once_with()
    self.assertNotEqual(
        m_state.State.return_value.log_level,
        logging.DEBUG,
    )

  @mock.patch(state.__name__ + ".state")
  def test_load_state_debug_logging(self, m_state: mock.Mock) -> None:
    self.instance.load_state(True)
    m_state.State.assert_called_once_with()
    m_state.State.return_value.load.assert_called_once_with()
    self.assertEqual(
        m_state.State.return_value.log_level,
        logging.DEBUG,
    )
