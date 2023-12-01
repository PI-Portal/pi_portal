"""Test the UploadVideoCommand class."""

import os
from unittest import mock

from pi_portal import config
from pi_portal.commands.bases.tests.fixtures import file_command_harness
from .. import upload_video
from ..mixins import state


class TestUploadVideoCommand(file_command_harness.FileCommandBaseTestHarness):
  """Test the UploadVideoCommand class.

  :param file_name: The path to a valid video file.
  """

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = upload_video.UploadVideoCommand

  def test_mixins(self) -> None:
    self.assertIsInstance(self.instance, state.CommandManagedStateMixin)

  @mock.patch(upload_video.__name__ + ".slack")
  def test_invoke(self, m_module: mock.Mock) -> None:

    with mock.patch(upload_video.__name__ + ".shutil.move") as m_move:
      self.instance.invoke()

    m_module.SlackClient.assert_called_once_with()
    m_module.SlackClient.return_value.send_file.assert_called_once_with(
        self.mock_file
    )
    m_move.assert_called_once_with(
        self.mock_file,
        os.path.join(
            config.VIDEO_UPLOAD_QUEUE_PATH,
            os.path.basename(self.mock_file),
        )
    )
