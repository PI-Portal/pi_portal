"""RotatingFileHandlerArchived class."""

import os
import threading
from datetime import datetime, timezone

from pi_portal import config
from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient
from .bases.rotation import RotatingFileHandlerBase


class RotatingFileHandlerArchived(RotatingFileHandlerBase):
  """Rotating file handler that adds post rotation archival."""

  post_rotation_queue_folder = config.PATH_QUEUE_LOG_UPLOAD

  def rotate(self, source: str, dest: str) -> None:
    """Perform the log rotation.

    :param source: The pre rotation file name of the log file.
    :param dest:  The post rotation file name of the log file.
    """

    super().rotate(source, dest)

    if os.path.exists(dest):
      task = threading.Thread(target=self.archive, args=[dest])
      task.start()

  def archive(self, dest: str) -> None:
    """Archive the rotated log file.

    :param dest:  The post rotation file name of the log file.
    """

    archival_filename = self.archival_filename()

    service_client = TaskSchedulerServiceClient()
    service_client.file_system_copy(
        dest,
        archival_filename,
    )

  def archival_filename(self) -> str:
    """Create an utc timestamped filename for archival."""

    timestamp = datetime.now().replace(tzinfo=timezone.utc).isoformat()
    archival_name = os.path.join(
        self.post_rotation_queue_folder,
        f"{timestamp}_{os.path.basename(self.baseFilename)}",
    )
    return archival_name
