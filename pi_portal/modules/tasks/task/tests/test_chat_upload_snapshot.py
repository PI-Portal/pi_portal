"""Test the chat_upload_snapshot module."""

import os

import pytest
from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import chat_upload_snapshot
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestChatUploadSnapshot(GenericTaskModuleTest):
  """Test the chat_upload_snapshot module."""

  expected_api_enabled = True
  expected_arg_class = chat_upload_snapshot.Args
  expected_return_type = None
  expected_type = enums.TaskType.CHAT_UPLOAD_SNAPSHOT
  mock_args = chat_upload_snapshot.Args(
      path=os.path.join(config.PATH_MOTION_CONTENT, "file1")
  )
  module = chat_upload_snapshot

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        chat_upload_snapshot.Args,
        ArgFileSystemRestrictionMixin,
    )

  def test_import__args_class__whitelist_attributes(self) -> None:
    assert chat_upload_snapshot.Args.file_system_arg_restrictions == {
        "path": [config.PATH_MOTION_CONTENT]
    }

  def test_import__args_class__initialize_with_invalid_args(self) -> None:
    with pytest.raises(ValueError):
      chat_upload_snapshot.Args(path="invalid_path1")
