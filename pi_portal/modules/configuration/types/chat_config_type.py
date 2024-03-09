"""Chat configuration types."""

from typing_extensions import TypedDict


class TypeUserConfigChat(TypedDict):
  """Typed representation of the chat configuration."""

  SLACK: "TypeUserConfigChatSlack"


class TypeUserConfigChatSlack(TypedDict):
  """Typed representation of the Slack chat configuration."""

  SLACK_APP_SIGNING_SECRET: str
  SLACK_APP_TOKEN: str
  SLACK_BOT_TOKEN: str
  SLACK_CHANNEL: str
  SLACK_CHANNEL_ID: str
  SLACK_FILE_TRANSFER_TIMEOUT: int
