"""Test the LogFileUploadCronJob class."""
import logging
import os
from datetime import datetime, timezone

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.integrations.s3 import client as s3_client
from ...bases import s3_upload_job
from .. import log_upload


class TestLogFileUploadCronJob:
  """Test the LogFileUploadCronJob class."""

  def test__initialization__attrs(
      self,
      log_upload_cron_job_instance: log_upload.LogFileUploadCronJob,
      mocked_cron_logger: logging.Logger,
      mocked_state: state.State,
  ) -> None:
    aws_config = mocked_state.user_config["ARCHIVAL"]["AWS"]
    assert log_upload_cron_job_instance.bucket_name == \
           aws_config["AWS_S3_BUCKETS"]["LOGS"]
    assert log_upload_cron_job_instance.interval == \
           config.CRON_INTERVAL_LOGS_UPLOAD
    assert log_upload_cron_job_instance.log == \
           mocked_cron_logger
    assert log_upload_cron_job_instance.name == \
           "Log File Upload"
    assert log_upload_cron_job_instance.path == \
           config.PATH_QUEUE_LOG_UPLOAD

  def test__initialization__inheritance(
      self,
      log_upload_cron_job_instance: log_upload.LogFileUploadCronJob,
  ) -> None:
    assert isinstance(
        log_upload_cron_job_instance,
        s3_upload_job.S3UploadCronJobBase,
    )

  def test__initialization__disk_queue(
      self,
      log_upload_cron_job_instance: log_upload.LogFileUploadCronJob,
  ) -> None:
    assert isinstance(
        log_upload_cron_job_instance.disk_queue,
        queue.DiskQueueIterator,
    )
    assert log_upload_cron_job_instance.disk_queue.path == \
        log_upload_cron_job_instance.path

  def test__initialization__s3_client(
      self,
      log_upload_cron_job_instance: log_upload.LogFileUploadCronJob,
      mocked_state: state.State,
  ) -> None:
    aws_config = mocked_state.user_config["ARCHIVAL"]["AWS"]
    assert isinstance(
        log_upload_cron_job_instance.s3_client,
        s3_client.S3BucketClient,
    )
    assert log_upload_cron_job_instance.s3_client.bucket_name == \
        aws_config["AWS_S3_BUCKETS"]["LOGS"]

  def test__object_name__correct_object_name(
      self,
      log_upload_cron_job_instance: log_upload.LogFileUploadCronJob,
  ) -> None:
    timestamp = datetime.now().replace(tzinfo=timezone.utc)
    lof_file_name = "mock.log"
    archival_name = os.path.join(
        config.PATH_QUEUE_LOG_UPLOAD,
        f"{timestamp.isoformat()}_{lof_file_name}",
    )

    object_name = log_upload_cron_job_instance.object_name(archival_name)

    assert object_name == os.path.join(
        timestamp.date().isoformat(),
        f"{timestamp.timetz().isoformat()}_{lof_file_name}",
    )
