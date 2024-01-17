"""S3UploadCronJobBase class."""

import logging
import os

from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.integrations.s3 import client
from .job import CronJobBase


class S3UploadCronJobBase(CronJobBase):
  """Cron job to upload content from a folder to S3.

  :param log: The logging instance for this cron job.
  """

  bucket_name: str
  disk_queue: queue.DiskQueueIterator
  interval: int
  path: str
  s3_client: client.S3BucketClient

  def __init__(self, log: logging.Logger) -> None:
    super().__init__(log)
    self.disk_queue = queue.DiskQueueIterator(self.path)
    self.s3_client = client.S3BucketClient(self.bucket_name)

  def cron(self) -> None:
    """Cron implementation."""

    for upload in self.disk_queue:
      obj_name = self.object_name(upload)
      try:
        self.log.info(
            "Uploading '%s' -> '%s' ...",
            upload,
            obj_name,
            extra={"job": self.name},
        )
        self.s3_client.upload(upload, obj_name)
        self.log.info(
            "Removing '%s' ...",
            upload,
            extra={"job": self.name},
        )
        os.remove(upload)
      except client.S3BucketException:
        self.log.error(
            "Failed to upload '%s' ...",
            upload,
            extra={"job": self.name},
        )
      except OSError:
        self.log.error(
            "Failed to remove '%s' ...",
            upload,
            extra={"job": self.name},
        )

  def object_name(self, file_name: str) -> str:
    """Override to derive an object name from the local file name.

    :param file_name: The name of the file being processed.
    :returns: The S3 object name that will be used.
    """

    return os.path.basename(file_name)
