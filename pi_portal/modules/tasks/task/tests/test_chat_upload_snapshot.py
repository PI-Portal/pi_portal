"""Test the chat_upload_snapshot module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_upload_snapshot
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatUploadSnapshot(GenericTaskModuleTest):
  """Test the chat_upload_snapshot module."""

  expected_api_enabled = True
  expected_arg_class = chat_upload_snapshot.Args
  expected_return_type = None
  expected_type = enums.TaskType.CHAT_UPLOAD_SNAPSHOT
  mock_args = chat_upload_snapshot.Args(path="/mock/path")
  module = chat_upload_snapshot
