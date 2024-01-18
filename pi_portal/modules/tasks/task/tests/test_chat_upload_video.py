"""Test the chat_upload_video module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_upload_video
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatUploadVideo(GenericTaskModuleTest):
  """Test the chat_upload_video module."""

  expected_api_enabled = True
  expected_arg_class = chat_upload_video.Args
  expected_return_type = None
  expected_type = enums.TaskType.CHAT_UPLOAD_VIDEO
  mock_args = chat_upload_video.Args(path="/mock/path")
  module = chat_upload_video
