"""Tests for the ChatConfigurationBase class."""

from typing import Dict

from pi_portal.modules.configuration import state
from ..config import TypeChatConfig


class TestChatConfigurationBase:
  """Tests for the ChatConfigurationBase class."""

  def test_initialize__attributes(
      self,
      mocked_user_config: Dict[str, str],
      concrete_chat_config_base_instance: TypeChatConfig,
  ) -> None:
    assert isinstance(
        concrete_chat_config_base_instance.current_state,
        state.State,
    )
    assert concrete_chat_config_base_instance.settings == mocked_user_config
    assert concrete_chat_config_base_instance.emoji_alert == (
        "mocked_emoji_alert"
    )
