"""Periodically creates a task to archive logs."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import archive_logs
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base


class CronJob(cron_job_base.CronJobBase[archive_logs.Args]):
  """Periodically creates a task to archive logs."""

  __slots__ = ()

  interval = config.CRON_INTERVAL_LOGS_UPLOAD
  name = "Archive Logs"
  type = enums.TaskType.ARCHIVE_LOGS

  def _args(self) -> archive_logs.Args:
    user_config = state.State().user_config
    aws_config = user_config["ARCHIVAL"]["AWS"]
    return archive_logs.Args(
        archival_path=config.PATH_QUEUE_LOG_UPLOAD,
        partition_name=aws_config["AWS_S3_BUCKETS"]["LOGS"]
    )
