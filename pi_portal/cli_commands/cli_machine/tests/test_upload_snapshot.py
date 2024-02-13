"""Test the UploadSnapshotCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import file_command
from pi_portal.cli_commands.cli_machine import upload_snapshot
from pi_portal.cli_commands.mixins import state


class TestUploadSnapshotCommand:
  """Test the UploadSnapshotCommand class."""

  def test_initialize__attributes(
      self,
      mocked_file_name: str,
      upload_snapshot_command_instance: upload_snapshot.UploadSnapshotCommand,
  ) -> None:
    assert upload_snapshot_command_instance.file_name == mocked_file_name

  def test_initialize__inheritance(
      self,
      upload_snapshot_command_instance: upload_snapshot.UploadSnapshotCommand,
  ) -> None:
    assert isinstance(
        upload_snapshot_command_instance, file_command.FileCommandBase
    )
    assert isinstance(
        upload_snapshot_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      mocked_file_name: str,
      mocked_slack_client: mock.Mock,
      upload_snapshot_command_instance: upload_snapshot.UploadSnapshotCommand,
  ) -> None:
    upload_snapshot_command_instance.invoke()

    mocked_slack_client.assert_called_once_with()
    mocked_slack_client.return_value.send_snapshot.assert_called_once_with(
        mocked_file_name
    )
