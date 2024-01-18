"""Periodically creates a task to archive videos."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import archive_videos
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base


class CronJob(cron_job_base.CronJobBase[archive_videos.Args]):
  """Periodically creates a task to archive videos."""

  __slots__ = ()

  interval = config.CRON_INTERVAL_VIDEO_UPLOAD
  name = "Archive Videos"
  type = enums.TaskType.ARCHIVE_VIDEOS

  def _args(self) -> archive_videos.Args:
    running_state = state.State()
    aws_config = running_state.user_config["ARCHIVAL"]["AWS"]
    return archive_videos.Args(
        archival_path=config.PATH_QUEUE_VIDEO_UPLOAD,
        partition_name=aws_config["AWS_S3_BUCKETS"]["VIDEOS"]
    )
