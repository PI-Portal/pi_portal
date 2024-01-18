"""Video archival task processor."""

import os
from threading import Lock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_archival


class ProcessorClass(processor_archival.ArchivalTaskProcessorBaseClass):
  """A task processor that uploads a video file to an archival service."""

  __slots__ = ()

  mutex = Lock()
  type = TaskType.ARCHIVE_VIDEOS

  def object_name(self, file_name: str) -> str:
    """Override to derive an object name from the local file name.

    :param file_name: The name of the file being processed.
    :returns: The S3 object name that will be used.
    """

    return os.path.basename(file_name)
