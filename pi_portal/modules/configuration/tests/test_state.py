"""Test RunningConfig monostate."""

import logging
from typing import cast
from unittest import mock

from pi_portal.modules.configuration import state, user_config


class TestRunningConfig:
  """Test the RunningConfig monostate."""

  mock_config = cast(user_config.TypeUserConfig, {"a": "b"})

  def test_instantiate__attrs(
      self,
      state_instance: state.State,
  ) -> None:
    assert state_instance.user_config == cast(user_config.TypeUserConfig, {})
    assert state_instance.log_level == logging.INFO
    assert isinstance(state_instance.log_uuid, str)

  def test_instantiate__enabled_debug__is_persistent(
      self,
      state_instance: state.State,
  ) -> None:
    state_instance.log_level = logging.DEBUG

    assert state_instance.log_level == logging.DEBUG

  def test_instantiate__mono_state__user_config_is_shared(
      self,
      state_instance: state.State,
      state_instance_clone: state.State,
  ) -> None:
    state_instance.user_config = cast(
        user_config.TypeUserConfig, {'test': 'value'}
    )

    assert state_instance.user_config == state_instance_clone.user_config

  def test_instantiate__mono_state__log_uuid_is_shared(
      self,
      state_instance: state.State,
      state_instance_clone: state.State,
  ) -> None:
    state_instance.log_uuid = "test id"

    assert state_instance.log_uuid == state_instance_clone.log_uuid

  def test_load_config__with_default_config__is_shared(
      self,
      mocked_user_configuration: mock.Mock,
      state_instance: state.State,
      state_instance_clone: state.State,
  ) -> None:
    mocked_user_configuration.return_value.user_config = self.mock_config

    state_instance.load()

    mocked_user_configuration.return_value.load.assert_called_once_with(
        file_path="config.json"
    )
    assert state_instance.user_config == self.mock_config
    assert state_instance.user_config == state_instance_clone.user_config

  def test_load_config__with_user_config_file__is_shared(
      self,
      mocked_user_configuration: mock.Mock,
      state_instance: state.State,
      state_instance_clone: state.State,
  ) -> None:
    mocked_user_configuration.return_value.user_config = self.mock_config

    state_instance.load("mock_file_path.json")

    mocked_user_configuration.return_value.load.assert_called_once_with(
        file_path="mock_file_path.json"
    )
    assert state_instance.user_config == self.mock_config
    assert state_instance.user_config == state_instance_clone.user_config
