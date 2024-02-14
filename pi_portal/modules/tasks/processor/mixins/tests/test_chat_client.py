"""Test the ChatClientMixin class."""

import pytest
from pi_portal.modules.integrations import slack
from pi_portal.modules.tasks.processor.mixins.chat_client import ChatClientMixin


@pytest.mark.usefixtures('test_state')
class TestChatClientMixin:
  """Test the ChatClientMixin class."""

  def test_initialize__slack_client(
      self,
      concrete_chat_mixin_instance: ChatClientMixin,
  ) -> None:
    assert concrete_chat_mixin_instance.chat_client_class == \
        slack.SlackClient
    assert isinstance(
        concrete_chat_mixin_instance.client,
        slack.SlackClient,
    )
