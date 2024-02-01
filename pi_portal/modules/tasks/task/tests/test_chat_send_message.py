"""Test the chat_send_message module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_send_message
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatSendMessage(GenericTaskModuleTest):
  """Test the chat_send_message module."""

  expected_api_enabled = True
  expected_arg_class = chat_send_message.Args
  expected_return_type = None
  expected_type = enums.TaskType.CHAT_SEND_MESSAGE
  mock_args = chat_send_message.Args(message="This is a test message.")
  module = chat_send_message
