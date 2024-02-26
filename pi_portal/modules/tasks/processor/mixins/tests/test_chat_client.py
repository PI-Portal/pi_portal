"""Test the ChatClientMixin class."""

import pytest
from pi_portal.modules.integrations.chat.service_client import ChatClient
from pi_portal.modules.tasks.processor.mixins.chat_client import ChatClientMixin


@pytest.mark.usefixtures('test_state')
class TestChatClientMixin:
  """Test the ChatClientMixin class."""

  def test_initialize__slack_client(
      self,
      concrete_chat_mixin_instance: ChatClientMixin,
  ) -> None:
    assert isinstance(
        concrete_chat_mixin_instance.client,
        ChatClient,
    )
    assert concrete_chat_mixin_instance.client.propagate_exceptions is True
