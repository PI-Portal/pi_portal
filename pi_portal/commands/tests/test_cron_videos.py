"""Test the CronVideosCommand class."""

from unittest import mock

from .. import cron_videos
from ..bases import command
from ..mixins import state


class TestCronVideosCommand:
  """Test the CronVideosCommand class."""

  def test_initialize__attributes(
      self,
      cron_videos_command_instance: cron_videos.CronVideosCommand,
  ) -> None:
    assert cron_videos_command_instance.interval == 30

  def test_initialize__inheritance(
      self,
      cron_videos_command_instance: cron_videos.CronVideosCommand,
  ) -> None:
    assert isinstance(cron_videos_command_instance, command.CommandBase)
    assert isinstance(
        cron_videos_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__calls(
      self,
      cron_videos_command_instance: cron_videos.CronVideosCommand,
      mocked_video_upload_cron: mock.Mock,
  ) -> None:
    cron_videos_command_instance.invoke()

    mocked_video_upload_cron.assert_called_once_with(
        cron_videos_command_instance.interval
    )
    mocked_video_upload_cron.return_value.start.assert_called_once_with()
