"""Test the UploadVideoCommand class."""

import os
from unittest import mock

from pi_portal import config
from .. import upload_video
from ..bases import file_command
from ..mixins import state


class TestUploadVideoCommand:
  """Test the UploadVideoCommand class."""

  def test_initialize__attributes(
      self,
      mocked_file_name: str,
      upload_video_command_instance: upload_video.UploadVideoCommand,
  ) -> None:
    assert upload_video_command_instance.file_name == mocked_file_name

  def test_initialize__inheritance(
      self,
      upload_video_command_instance: upload_video.UploadVideoCommand,
  ) -> None:
    assert isinstance(
        upload_video_command_instance, file_command.FileCommandBase
    )
    assert isinstance(
        upload_video_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      mocked_file_name: str,
      mocked_slack_client: mock.Mock,
      mocked_shutil: mock.Mock,
      upload_video_command_instance: upload_video.UploadVideoCommand,
  ) -> None:
    upload_video_command_instance.invoke()

    mocked_slack_client.assert_called_once_with()
    mocked_slack_client.return_value.send_file.assert_called_once_with(
        mocked_file_name
    )
    mocked_shutil.move.assert_called_once_with(
        mocked_file_name,
        os.path.join(
            config.PATH_QUEUE_VIDEO_UPLOAD,
            os.path.basename(mocked_file_name),
        )
    )
