"""Log file archival task processor."""

import os
from datetime import datetime
from threading import Lock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_archival


class ProcessorClass(
    processor_archival.ArchivalTaskProcessorBaseClass,
):
  """A task processor that uploads a file to an archival service."""

  __slots__ = ()

  mutex = Lock()
  type = TaskType.ARCHIVE_LOGS

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
