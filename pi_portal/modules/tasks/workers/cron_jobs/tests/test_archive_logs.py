"""Test the archive_logs class."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.archive_logs import Args
from .. import archive_logs
from ..bases import cron_job_base


class TestArchiveLogsCronJob:
  """Test the archive_logs class."""

  def test_initialize__attributes(
      self,
      archive_logs_cron_job_instance: archive_logs.CronJob,
  ) -> None:
    assert archive_logs_cron_job_instance.interval == \
        config.CRON_INTERVAL_LOGS_UPLOAD
    assert archive_logs_cron_job_instance.name == "Archive Logs"
    assert archive_logs_cron_job_instance.quiet is False
    assert archive_logs_cron_job_instance.type == \
        enums.TaskType.ARCHIVE_LOGS
    assert archive_logs_cron_job_instance.priority == \
        enums.TaskPriority.STANDARD

  def test_initialize__inheritance(
      self,
      archive_logs_cron_job_instance: archive_logs.CronJob,
  ) -> None:
    assert isinstance(
        archive_logs_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      archive_logs_cron_job_instance: archive_logs.CronJob,
      test_state: state.State,
  ) -> None:
    aws_config = test_state.user_config["ARCHIVAL"]["AWS"]
    expected_args = Args(partition_name=aws_config["AWS_S3_BUCKETS"]["LOGS"])

    # pylint: disable=protected-access
    assert archive_logs_cron_job_instance._args() == expected_args
