"""Test the CommandManagedStateMixin class."""

import logging
from unittest import mock

from pi_portal import config
from .. import state


class TestCommandManagedStateMixin:
  """Test the CommandManagedStateMixin class."""

  debug_subtests = [False, True]

  def check_logging_level(
      self,
      debug_value: bool,
      m_state: mock.Mock,
  ) -> None:
    current_log_level = m_state.return_value.log_level
    if debug_value:
      assert current_log_level == logging.DEBUG
    else:
      assert current_log_level != logging.DEBUG

  def test_load_state__default_config__no_specified_config(
      self,
      command_managed_state_mixin_instance: state.CommandManagedStateMixin,
      mocked_state: mock.Mock,
  ) -> None:
    for debug_value in self.debug_subtests:
      mocked_state.reset_mock()

      command_managed_state_mixin_instance.load_state(debug_value)

      mocked_state.assert_called_once_with()
      mocked_state.return_value.load.assert_called_once_with(
          file_path=config.PATH_USER_CONFIG
      )
      self.check_logging_level(debug_value, mocked_state)

  def test_load_state__default_config__specified_config(
      self,
      command_managed_state_mixin_instance: state.CommandManagedStateMixin,
      mocked_state: mock.Mock,
  ) -> None:
    for debug_value in self.debug_subtests:
      mocked_state.reset_mock()

      command_managed_state_mixin_instance.load_state(
          debug_value, file_path="mock_file_path.json"
      )

      mocked_state.assert_called_once_with()
      mocked_state.return_value.load.assert_called_once_with(
          file_path="mock_file_path.json"
      )
      self.check_logging_level(debug_value, mocked_state)

  def test_load_state__user_config_file__no_specified_config(
      self,
      command_managed_state_mixin_instance: state.CommandManagedStateMixin,
      mocked_state: mock.Mock,
  ) -> None:
    for debug_value in self.debug_subtests:
      mocked_state.reset_mock()

      command_managed_state_mixin_instance.load_state(debug_value)

      mocked_state.assert_called_once_with()
      mocked_state.return_value.load.assert_called_once_with(
          file_path=config.PATH_USER_CONFIG
      )
      self.check_logging_level(debug_value, mocked_state)

  def test_load_state__user_config_file__specified_config(
      self,
      command_managed_state_mixin_instance: state.CommandManagedStateMixin,
      mocked_state: mock.Mock,
  ) -> None:
    for debug_value in self.debug_subtests:
      mocked_state.reset_mock()

      command_managed_state_mixin_instance.load_state(
          debug_value, "mock_file_path.json"
      )

      mocked_state.assert_called_once_with()
      mocked_state.return_value.load.assert_called_once_with(
          file_path="mock_file_path.json"
      )
      self.check_logging_level(debug_value, mocked_state)
