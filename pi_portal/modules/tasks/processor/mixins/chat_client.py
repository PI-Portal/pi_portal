"""A chat client for chat task processors."""
from typing import Any, Type

from pi_portal.modules.integrations.chat import TypeChatClient
from pi_portal.modules.integrations.chat.service_client import ChatClient


class ChatClientMixin:
  """A chat client for chat task processors."""

  chat_client_class: Type[TypeChatClient] = ChatClient

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.client = self.chat_client_class()
    super().__init__(*args, **kwargs)
