"""Test the CommandManagedStateMixin class."""

import logging
from unittest import TestCase, mock

from pi_portal import config
from .. import state


class TestLoadStateCommand(TestCase):
  """Test the CommandManagedStateMixin class."""

  debug_subtests = [False, True]

  def setUp(self) -> None:
    self.instance = state.CommandManagedStateMixin()

  def check_logging_level(
      self,
      debug_value: bool,
      m_state: mock.Mock,
  ) -> None:
    current_log_level = m_state.State.return_value.log_level
    if debug_value:
      assert current_log_level == logging.DEBUG
    else:
      assert current_log_level != logging.DEBUG

  @mock.patch(state.__name__ + ".state")
  def test_load_state__default_config__no_specified_config(
      self, m_state: mock.Mock
  ) -> None:
    for debug_value in self.debug_subtests:
      m_state.reset_mock()

      self.instance.load_state(debug_value)

      m_state.State.assert_called_once_with()
      m_state.State.return_value.load.assert_called_once_with(
          file_path=config.PATH_USER_CONFIG_INSTALL
      )
      self.check_logging_level(debug_value, m_state)

  @mock.patch(state.__name__ + ".state")
  def test_load_state__default_config__specified_config(
      self, m_state: mock.Mock
  ) -> None:
    for debug_value in self.debug_subtests:
      m_state.reset_mock()

      self.instance.load_state(debug_value, file_path="mock_file_path.json")

      m_state.State.assert_called_once_with()
      m_state.State.return_value.load.assert_called_once_with(
          file_path="mock_file_path.json"
      )
      self.check_logging_level(debug_value, m_state)

  @mock.patch(state.__name__ + ".state")
  def test_load_state__user_config_file__no_specified_config(
      self, m_state: mock.Mock
  ) -> None:
    for debug_value in self.debug_subtests:
      m_state.reset_mock()

      self.instance.load_state(debug_value)

      m_state.State.assert_called_once_with()
      m_state.State.return_value.load.assert_called_once_with(
          file_path=config.PATH_USER_CONFIG_INSTALL
      )
      self.check_logging_level(debug_value, m_state)

  @mock.patch(state.__name__ + ".state")
  def test_load_state__user_config_file__specified_config(
      self, m_state: mock.Mock
  ) -> None:
    for debug_value in self.debug_subtests:
      m_state.reset_mock()

      self.instance.load_state(debug_value, "mock_file_path.json")

      m_state.State.assert_called_once_with()
      m_state.State.return_value.load.assert_called_once_with(
          file_path="mock_file_path.json"
      )
      self.check_logging_level(debug_value, m_state)
