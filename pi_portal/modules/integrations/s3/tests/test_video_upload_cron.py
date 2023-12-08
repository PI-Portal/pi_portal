"""Test the VideoUploadCron class."""

from pi_portal import config
from pi_portal.modules.integrations.s3 import video_upload_cron
from pi_portal.modules.integrations.s3.bases import cron
from pi_portal.modules.mixins import write_log_file


class TestVideoUploadCron:
  """Test the VideoUploadCron class."""

  def test__initialization__attrs(
      self,
      video_upload_queue_instance: video_upload_cron.VideoUploadCron,
  ) -> None:
    assert video_upload_queue_instance.path == config.PATH_VIDEO_UPLOAD_QUEUE
    assert video_upload_queue_instance.log_file_path == \
           config.LOG_FILE_VIDEO_UPLOAD_CRON
    assert video_upload_queue_instance.logger_name == "video_upload_cron"

  def test__initialization__inheritance(
      self,
      video_upload_queue_instance: video_upload_cron.VideoUploadCron,
  ) -> None:
    assert isinstance(video_upload_queue_instance, cron.S3UploadCronJobBase)
    assert isinstance(video_upload_queue_instance, write_log_file.LogFileWriter)
