"""A chat client for chat task processors."""
from typing import Any

from pi_portal.modules.integrations import slack


class ChatClientMixin:
  """A chat client for chat task processors."""

  chat_client_class = slack.SlackClient

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.client = self.chat_client_class()
    super().__init__(*args, **kwargs)
