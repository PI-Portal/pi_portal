"""Configuration for the Slack integration."""

from pi_portal.modules.configuration.types.chat_config_type import (
    TypeUserConfigChatSlack,
)
from pi_portal.modules.integrations.chat.bases.config import (
    ChatConfigurationBase,
)


class SlackIntegrationConfiguration(
    ChatConfigurationBase[TypeUserConfigChatSlack]
):
  """Configuration for the Slack integration."""

  emoji_alert = ":rotating_light:"
  settings: TypeUserConfigChatSlack

  def __init__(self) -> None:
    super().__init__()
    self.settings = self.current_state.user_config["CHAT"]["SLACK"]
