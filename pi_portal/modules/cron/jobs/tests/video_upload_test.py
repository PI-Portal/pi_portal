"""Test the VideoUploadCronJob class."""
import logging

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.integrations.s3 import client as s3_client
from ...bases import job, s3_upload_job
from .. import video_upload


class TestVideoUploadCron:
  """Test the VideoUploadCronJob class."""

  def test__initialization__attrs(
      self,
      video_upload_cron_job_instance: video_upload.VideoUploadCronJob,
      mocked_cron_logger: logging.Logger,
      mocked_state: state.State,
  ) -> None:
    aws_config = mocked_state.user_config["ARCHIVAL"]["AWS"]
    assert video_upload_cron_job_instance.bucket_name == \
           aws_config["AWS_S3_BUCKETS"]["VIDEOS"]
    assert video_upload_cron_job_instance.interval == \
           config.CRON_INTERVAL_VIDEO_UPLOAD
    assert video_upload_cron_job_instance.log == \
           mocked_cron_logger
    assert video_upload_cron_job_instance.name == \
           "Video Upload"
    assert video_upload_cron_job_instance.path == \
           config.PATH_QUEUE_VIDEO_UPLOAD

  def test__initialization__inheritance(
      self,
      video_upload_cron_job_instance: video_upload.VideoUploadCronJob,
  ) -> None:
    assert isinstance(
        video_upload_cron_job_instance,
        s3_upload_job.S3UploadCronJobBase,
    )
    assert isinstance(
        video_upload_cron_job_instance,
        job.CronJobBase,
    )

  def test__initialization__disk_queue(
      self,
      video_upload_cron_job_instance: video_upload.VideoUploadCronJob,
  ) -> None:
    assert isinstance(
        video_upload_cron_job_instance.disk_queue,
        queue.DiskQueueIterator,
    )
    assert video_upload_cron_job_instance.disk_queue.path == \
        video_upload_cron_job_instance.path

  def test__initialization__s3_client(
      self,
      video_upload_cron_job_instance: video_upload.VideoUploadCronJob,
      mocked_state: state.State,
  ) -> None:
    aws_config = mocked_state.user_config["ARCHIVAL"]["AWS"]
    assert isinstance(
        video_upload_cron_job_instance.s3_client,
        s3_client.S3BucketClient,
    )
    assert video_upload_cron_job_instance.s3_client.bucket_name == \
        aws_config["AWS_S3_BUCKETS"]["VIDEOS"]
