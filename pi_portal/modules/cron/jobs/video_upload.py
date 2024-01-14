"""VideoUploadCronJob class."""

from pi_portal import config
from ..bases import s3_upload_job


class VideoUploadCronJob(s3_upload_job.S3UploadCronJobBase):
  """S3 upload cron for motion video file archival.

  :param interval: The interval in seconds to check for new files.
  """

  interval = config.CRON_INTERVAL_VIDEO_UPLOAD
  name = "Video Upload"
  path = config.PATH_VIDEO_UPLOAD_QUEUE
