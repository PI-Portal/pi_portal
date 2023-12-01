"""Test the CronVideosCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import command_harness
from .. import cron_videos
from ..mixins import state

CRON_VIDEOS_MODULE = cron_videos.__name__


class TestCronVideosCommand(command_harness.CommandBaseTestHarness):
  """Test the CronVideosCommand class."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = cron_videos.CronVideosCommand

  def test_attr(self) -> None:
    self.assertEqual(cron_videos.CronVideosCommand.interval, 30)

  def test_mixins(self) -> None:
    self.assertIsInstance(self.instance, state.CommandManagedStateMixin)

  @mock.patch(CRON_VIDEOS_MODULE + ".video_upload_cron.VideoUploadCron")
  def test_invoke(self, m_module: mock.Mock) -> None:

    self.instance.invoke()

    m_module.assert_called_once_with(cron_videos.CronVideosCommand.interval)
    m_module.return_value.start.assert_called_once_with()
