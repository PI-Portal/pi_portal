"""Test the archive_videos module."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.archive_videos import Args
from .. import archive_videos
from ..bases import cron_job_base


class TestArchiveVideosCronJob:
  """Test the archive_videos module."""

  def test_initialize__attributes(
      self,
      archive_videos_cron_job_instance: archive_videos.CronJob,
  ) -> None:
    assert archive_videos_cron_job_instance.interval == \
        config.CRON_INTERVAL_VIDEO_UPLOAD
    assert archive_videos_cron_job_instance.name == "Archive Videos"
    assert archive_videos_cron_job_instance.quiet is False
    assert archive_videos_cron_job_instance.type == \
        enums.TaskType.ARCHIVE_VIDEOS
    assert archive_videos_cron_job_instance.priority == \
        enums.TaskPriority.STANDARD

  def test_initialize__inheritance(
      self,
      archive_videos_cron_job_instance: archive_videos.CronJob,
  ) -> None:
    assert isinstance(
        archive_videos_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      archive_videos_cron_job_instance: archive_videos.CronJob,
      mocked_state: state.State,
  ) -> None:
    aws_config = mocked_state.user_config["ARCHIVAL"]["AWS"]
    expected_args = Args(partition_name=aws_config["AWS_S3_BUCKETS"]["VIDEOS"])

    # pylint: disable=protected-access
    assert archive_videos_cron_job_instance._args() == expected_args
