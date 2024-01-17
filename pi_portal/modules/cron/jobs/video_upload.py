"""VideoUploadCronJob class."""

import logging

from pi_portal import config
from pi_portal.modules.configuration import state
from ..bases import s3_upload_job


class VideoUploadCronJob(s3_upload_job.S3UploadCronJobBase):
  """S3 upload cron for motion video file archival.

  :param log: The logging instance for this cron job.
  """

  interval = config.CRON_INTERVAL_VIDEO_UPLOAD
  name = "Video Upload"
  path = config.PATH_QUEUE_VIDEO_UPLOAD

  def __init__(self, log: logging.Logger) -> None:
    running_state = state.State()
    aws_config = running_state.user_config["ARCHIVAL"]["AWS"]
    self.bucket_name = aws_config["AWS_S3_BUCKETS"]["VIDEOS"]
    super().__init__(log)
