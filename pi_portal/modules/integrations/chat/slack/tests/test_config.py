"""Test the SlackClientConfiguration class."""
import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.bases.config import (
    ChatConfigurationBase,
)
from pi_portal.modules.integrations.chat.slack import config


@pytest.mark.usefixtures("test_state")
class TestSlackClient:
  """Test the SlackClientConfiguration class."""

  def test_initialize__attributes(
      self,
      slack_configuration_instance: config.SlackIntegrationConfiguration,
      test_state: state.State,
  ) -> None:
    assert slack_configuration_instance.settings == (
        test_state.user_config["CHAT"]["SLACK"]
    )

  def test_initialize__inheritance(
      self,
      slack_configuration_instance: config.SlackIntegrationConfiguration,
  ) -> None:
    assert isinstance(
        slack_configuration_instance,
        config.SlackIntegrationConfiguration,
    )
    assert isinstance(
        slack_configuration_instance,
        ChatConfigurationBase,
    )
