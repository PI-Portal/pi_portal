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

  disk_queue: queue.DiskQueueIterator
  interval: int
  path: str
  s3_client: client.S3BucketClient

  def __init__(self, log: logging.Logger) -> None:
    super().__init__(log)
    self.disk_queue = queue.DiskQueueIterator(self.path)
    self.s3_client = client.S3BucketClient()

  def cron(self) -> None:
    """Cron implementation."""

    for upload in self.disk_queue:
      try:
        self.log.info(
            "Uploading '%s' ...",
            upload,
            extra={"job": self.name},
        )
        self.s3_client.upload(upload)
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
