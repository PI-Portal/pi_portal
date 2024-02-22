"""Test the UploadVideoCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import file_command
from pi_portal.cli_commands.cli_machine import upload_video
from pi_portal.cli_commands.mixins import state


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
      mocked_task_scheduler_service_client: mock.Mock,
      upload_video_command_instance: upload_video.UploadVideoCommand,
  ) -> None:
    upload_video_command_instance.invoke()

    mocked_task_scheduler_service_client.assert_called_once_with()
    mocked_task_scheduler_service_client.return_value.\
        chat_upload_video.assert_called_once_with(
            mocked_file_name,
        )
