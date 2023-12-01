"""VideoUploadCron class."""

from pi_portal import config
from .bases import cron


class VideoUploadCron(cron.S3UploadCronJobBase):
  """S3 upload cron for motion video files.

  :param interval: The interval in seconds to check for new files.
  """

  path = config.VIDEO_UPLOAD_QUEUE_PATH
  log_file_path = config.VIDEO_UPLOAD_QUEUE_LOGFILE_PATH
  logger_name = "video_upload_cron"
