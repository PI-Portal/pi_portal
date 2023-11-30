"""S3UploadCronJobBase class."""

import os
import time

from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.integrations.s3 import client
from pi_portal.modules.mixins import write_log_file


class S3UploadCronJobBase(write_log_file.LogFileWriter):
  """Persistent cron job to upload content from a folder to S3.

  :param interval: The interval in seconds to check for new files.
  """

  disk_queue: queue.DiskQueueIterator
  interval: int
  log_file_path: str
  logger_name: str
  path: str
  s3_client: client.S3BucketClient

  def __init__(self, interval: int) -> None:
    self.configure_logger()
    self.disk_queue = queue.DiskQueueIterator(self.path)
    self.interval = interval
    self.s3_client = client.S3BucketClient()

  def start(self) -> None:
    """Start the upload cron."""

    self.log.warning("%s is starting ...", self.__class__.__name__)

    while True:
      self._cron()

  def _cron(self) -> None:

    for upload in self.disk_queue:
      try:
        self.log.info("Uploading '%s' ...", upload)
        self.s3_client.upload(upload)
        self.log.info("Removing '%s' ...", upload)
        os.remove(upload)
      except client.S3BucketException:
        self.log.error("Failed to upload '%s' ...", upload)
      except OSError:
        self.log.error("Failed to remove '%s' ...", upload)

    time.sleep(self.interval)
