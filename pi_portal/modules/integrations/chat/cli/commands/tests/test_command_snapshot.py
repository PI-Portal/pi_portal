"""Test the SnapshotCommand class."""

from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.cli.commands import SnapshotCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases import process_command


@pytest.mark.usefixtures("test_state")
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

  @pytest.mark.parametrize("camera_count", [1, 2, 3])
  def test_invoke__process_is_running__takes_snapshot(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_supervisor_process: mock.Mock,
      mocked_chat_bot: mock.Mock,
      test_state: state.State,
      camera_count: int,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = True
    test_state.user_config["CAMERA"]["MOTION"]["CAMERAS"] = (
        test_state.user_config["CAMERA"]["MOTION"]["CAMERAS"] * camera_count
    )
    expected_calls = [
        mock.call(camera=index) for index in range(0, camera_count)
    ]

    snapshot_command_instance.invoke()

    assert (
        mocked_chat_bot.task_scheduler_client.camera_snapshot.mock_calls ==
        expected_calls
    )

  def test_invoke__process_is_running__sends_notification(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_supervisor_process: mock.Mock,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = True

    snapshot_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client. \
        chat_send_message.assert_called_once_with(
          "Processing snapshot request ..."
        )

  def test_invoke__process_not_running__does_not_take_snapshot(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_supervisor_process: mock.Mock,
      mocked_task_scheduler_client: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = False

    snapshot_command_instance.invoke()

    mocked_task_scheduler_client.camera_snapshot.assert_not_called()

  def test_invoke__process_not_running__sends_notification(
      self,
      snapshot_command_instance: SnapshotCommand,
      mocked_chat_bot: mock.Mock,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    mocked_supervisor_process.return_value.status_in.return_value = False

    snapshot_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client. \
        chat_send_message.assert_called_once_with(
          "Please `arm` the camera first ..."
        )
