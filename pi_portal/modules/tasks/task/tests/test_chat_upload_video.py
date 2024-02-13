"""Test the chat_upload_video module."""

import os

import pytest
from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_upload_video
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatUploadVideo(GenericTaskModuleTest):
  """Test the chat_upload_video module."""

  expected_api_enabled = True
  expected_arg_class = chat_upload_video.Args
  expected_return_type = None
  expected_type = enums.TaskType.CHAT_UPLOAD_VIDEO
  mock_args = chat_upload_video.Args(
      description="Test file number 1.",
      path=os.path.join(config.PATH_MOTION_CONTENT, "file1")
  )
  module = chat_upload_video

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        chat_upload_video.Args,
        ArgFileSystemRestrictionMixin,
    )

  def test_import__args_class__whitelist(self) -> None:
    assert chat_upload_video.Args.file_system_arg_restrictions == {
        "path": [config.PATH_MOTION_CONTENT]
    }

  def test_import__args_class__initialize_with_invalid_args(self) -> None:
    with pytest.raises(ValueError):
      chat_upload_video.Args(
          description="A file from a restricted path.",
          path="invalid_path1",
      )
