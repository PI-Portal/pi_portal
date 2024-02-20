"""Test the SnapshotCommand class."""

from unittest import mock

from pi_portal.modules.integrations.motion import client as motion_client
from pi_portal.modules.integrations.slack.cli.commands import SnapshotCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases import process_command


class TestSnapshotCommand:
  """Test the SnapshotCommand class."""

  def test_initialize__attributes(
      self,
      snapshot_command_instance: SnapshotCommand,
  ) -> None:
    assert snapshot_command_instance.process_name == ProcessList.CAMERA

  def test_initialize__inheritance(
      self,
      snapshot_command_instance: SnapshotCommand,
  ) -> None:
    assert isinstance(
        snapshot_command_instance,
        process_command.ChatProcessCommandBase,
    )

  def test_initialize__motion_client(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_chat_bot: mock.Mock,
      mocked_motion_client: mock.Mock,
  ) -> None:
    assert snapshot_command_instance.motion_client == (
        mocked_motion_client.return_value
    )
    mocked_motion_client.assert_called_once_with(mocked_chat_bot.log)

  def test_invoke__process_is_running__no_error__takes_snapshot(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_supervisor_process: mock.Mock,
      mocked_motion_client: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = True

    snapshot_command_instance.invoke()

    mocked_motion_client.return_value.take_snapshot.assert_called_once_with()

  def test_invoke__process_is_running__error__raises_exception(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_cli_notifier: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      mocked_motion_client: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = True
    mocked_motion_client.return_value.take_snapshot.side_effect = (
        motion_client.MotionException("Boom!")
    )

    snapshot_command_instance.invoke()

    mocked_cli_notifier.return_value.notify_error.assert_called_once_with()

  def test_invoke__process_not_running__no_error__does_not_take_snapshot(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_supervisor_process: mock.Mock,
      mocked_motion_client: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = False

    snapshot_command_instance.invoke()

    mocked_motion_client.return_value.take_snapshot.assert_not_called()

  def test_invoke__process_not_running__no_error__sends_notification(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_chat_bot: mock.Mock,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = False

    snapshot_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "Please `arm` the camera first ..."
    )
