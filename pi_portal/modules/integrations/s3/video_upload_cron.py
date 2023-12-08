"""VideoUploadCron class."""

from pi_portal import config
from .bases import cron


class VideoUploadCron(cron.S3UploadCronJobBase):
  """S3 upload cron for motion video files.

  :param interval: The interval in seconds to check for new files.
  """

  path = config.PATH_VIDEO_UPLOAD_QUEUE
  log_file_path = config.LOG_FILE_VIDEO_UPLOAD_CRON
  logger_name = "video_upload_cron"
