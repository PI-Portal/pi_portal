"""Test the UploadSnapshotCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import file_command_harness
from .. import upload_snapshot


class TestUploadSnapshotCommand(
    file_command_harness.FileCommandBaseTestHarness
):
  """Test the UploadSnapshotCommand class.

  :param file_name: The path to a valid snapshot file.
  """

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = upload_snapshot.UploadSnapshotCommand

  @mock.patch(upload_snapshot.__name__ + ".slack")
  def test_invoke(self, m_module: mock.Mock) -> None:
    self.instance.invoke()
    m_module.SlackClient.assert_called_once_with()
    m_module.SlackClient.return_value.send_snapshot.assert_called_once_with(
        self.mock_file
    )
