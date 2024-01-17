"""LogFileUploadCronJob class."""

import logging
import os
from datetime import datetime

from pi_portal import config
from pi_portal.modules.configuration import state
from ..bases import s3_upload_job


class LogFileUploadCronJob(s3_upload_job.S3UploadCronJobBase):
  """S3 upload cron for log file archival.

  :param log: The logging instance for this cron job.
  """

  interval = config.CRON_INTERVAL_LOGS_UPLOAD
  name = "Log File Upload"
  path = config.PATH_QUEUE_LOG_UPLOAD

  def __init__(self, log: logging.Logger) -> None:
    running_state = state.State()
    aws_config = running_state.user_config["ARCHIVAL"]["AWS"]
    self.bucket_name = aws_config["AWS_S3_BUCKETS"]["LOGS"]
    super().__init__(log)

  def object_name(self, file_name: str) -> str:
    """Extract a timestamp and logfile name.

    :param file_name: The name of the file being processed.
    :returns: The S3 object name that will be used.
    """
    base_name = os.path.basename(file_name)
    parsed_file_name = base_name.split("_")
    timestamp = datetime.fromisoformat(parsed_file_name[0])
    log_name = "".join(parsed_file_name[1:])

    return os.path.join(
        timestamp.date().isoformat(),
        f"{timestamp.timetz().isoformat()}_{log_name}"
    )
