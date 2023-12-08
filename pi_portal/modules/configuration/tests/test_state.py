"""Test RunningConfig monostate."""

import logging
from typing import cast
from unittest import TestCase, mock

from pi_portal.modules.configuration import state, user_config


class TestRunningConfig(TestCase):
  """Test the RunningConfig monostate."""

  def setUp(self) -> None:
    self.instance = state.State()

  def test_instantiate__attrs(self) -> None:
    instance = state.State()
    self.assertEqual(instance.user_config, {})
    self.assertEqual(instance.log_level, logging.INFO)
    self.assertIsInstance(instance.log_uuid, str)

  def test_instantiate__debug_enabled(self) -> None:
    self.instance.log_level = logging.DEBUG
    self.assertEqual(self.instance.log_level, logging.DEBUG)
    self.instance.log_level = logging.INFO

  def test_instantiate__mono_state_user_config(self) -> None:
    self.instance.user_config = cast(
        user_config.TypeUserConfig, {'test': 'value'}
    )

    instance2 = state.State()
    self.assertEqual(
        self.instance.user_config, getattr(instance2, 'user_config')
    )

  def test_instantiate__mono_state_log_uuid(self) -> None:
    self.instance.log_uuid = "test id"

    instance2 = state.State()
    self.assertEqual(self.instance.log_uuid, getattr(instance2, 'log_uuid'))

  @mock.patch(state.__name__ + ".UserConfiguration")
  def test_load_config__default(self, m_user_config: mock.Mock) -> None:
    mock_config = {
        "a": "b"
    }
    m_user_config.return_value.user_config = mock_config

    self.instance.load()

    m_user_config.return_value.load.assert_called_once_with(
        file_path="config.json"
    )
    self.assertEqual(self.instance.user_config, mock_config)

    instance2 = state.State()
    self.assertEqual(self.instance.user_config, instance2.user_config)

  @mock.patch(state.__name__ + ".UserConfiguration")
  def test_load_config__user_config_file(
      self, m_user_config: mock.Mock
  ) -> None:
    mock_config = {
        "a": "b"
    }
    m_user_config.return_value.user_config = mock_config

    self.instance.load("mock_file_path.json")

    m_user_config.return_value.load.assert_called_once_with(
        file_path="mock_file_path.json"
    )
    self.assertEqual(self.instance.user_config, mock_config)

    instance2 = state.State()
    self.assertEqual(self.instance.user_config, instance2.user_config)
