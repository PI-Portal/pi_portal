"""Test the Slack CLI Snapshot Command."""

from typing import Type, cast
from unittest import mock

from pi_portal.modules.integrations import motion
from pi_portal.modules.integrations.slack_cli.commands import command_snapshot
from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from ..bases.tests.fixtures import process_command_harness


class TestSnapshotCommand(
    process_command_harness.ProcessCommandBaseTestHarness
):
  """Test the Slack CLI Snapshot Command."""

  __test__ = True
  expected_process_name = ProcessList.CAMERA
  expected_process_command: Literal["status_in"] = "status_in"

  def _mock_motion_client(self) -> mock.Mock:
    return cast(mock.Mock, self.mock_motion_client.return_value)

  def get_test_class(self) -> Type[command_snapshot.SnapshotCommand]:
    return command_snapshot.SnapshotCommand

  def setUp(self) -> None:
    with mock.patch(
        command_snapshot.__name__ + ".motion.Motion"
    ) as mock_motion_client:
      self.mock_motion_client = mock_motion_client
      super().setUp()

  def test_invoke(self) -> None:
    self._mocked_process().status_in.return_value = True
    self.instance.invoke()
    self._mock_motion_client().take_snapshot.assert_called_once_with()

  def test_invoke_motion_error(self) -> None:
    self._mocked_process().status_in.return_value = True
    self._mock_motion_client().take_snapshot.side_effect = \
      motion.MotionException("Boom!")
    self.instance.invoke()
    self.mock_notifier.notify_error.assert_called_once_with()

  def test_invoke_not_running(self) -> None:
    self._mocked_process().status_in.return_value = False
    self.instance.invoke()
    self._mock_motion_client().take_snapshot.assert_not_called()
    self.mock_slack_client.send_message.assert_called_once_with(
        "Please `arm` the camera first ..."
    )
