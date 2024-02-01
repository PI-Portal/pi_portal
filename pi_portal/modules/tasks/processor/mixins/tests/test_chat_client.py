"""Test the ChatClientMixin class."""

from pi_portal.modules.integrations import slack
from pi_portal.modules.tasks.processor.mixins.chat_client import ChatClientMixin


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
