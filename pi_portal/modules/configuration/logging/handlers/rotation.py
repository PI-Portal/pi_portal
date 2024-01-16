"""RotatingFileHandlerWithEnqueue class."""

import os
import shutil
import threading
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from pi_portal import config
from pi_portal.modules.system import file_system


class RotatingFileHandlerWithEnqueue(RotatingFileHandler):
  """Rotating file handler that adds post rotation task enqueuing."""

  post_rotation_queue_folder = config.PATH_QUEUE_LOG_UPLOAD

  def __init__(self, filename: str):
    super().__init__(
        filename,
        backupCount=3,
        delay=True,
        encoding="utf-8",
        maxBytes=10000000,  # 10MB
    )

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

    shutil.copy(
        dest,
        archival_filename,
    )
    fs = file_system.FileSystem(archival_filename)
    fs.permissions("640")

  def archival_filename(self) -> str:
    """Create an utc timestamped filename for archival."""

    timestamp = datetime.now().replace(tzinfo=timezone.utc).isoformat()
    archival_name = os.path.join(
        self.post_rotation_queue_folder,
        f"{timestamp}_{os.path.basename(self.baseFilename)}",
    )
    return archival_name
