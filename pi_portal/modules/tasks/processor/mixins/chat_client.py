"""A chat client for chat task processors."""
from typing import Any

from pi_portal.modules.integrations.chat.service_client import ChatClient


class ChatClientMixin:
  """A chat client for chat task processors."""

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.client = ChatClient(propagate_exceptions=True)
    super().__init__(*args, **kwargs)
