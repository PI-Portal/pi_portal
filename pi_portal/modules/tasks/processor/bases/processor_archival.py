"""Archival task processor base class."""

import os
from threading import Lock
from typing import TYPE_CHECKING

from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import archival_client
from pi_portal.modules.tasks.task.shared.archive import ArchivalTaskArgs

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TaskBase


class ArchivalTaskProcessorBaseClass(
    archival_client.ArchivalClientMixin,
    processor_base.TaskProcessorBase["ArchivalTaskArgs", None]
):
  """A task processor that uploads files to an archival service."""

  __slots__ = ()

  disk_queue_class = queue.DiskQueueIterator
  mutex: Lock

  def _process(
      self,
      task: "processor_base.TaskBase[ArchivalTaskArgs, None]",
  ) -> None:
    if self.mutex.locked():
      self.log.info(
          "Mutex is locked, aborting '%s' cron run ...",
          task,
          extra={"task": task.id},
      )
      return None

    with self.mutex:
      disk_queue = self.disk_queue_class(task.args.archival_path)
      client = self.archival_client_class(task.args.partition_name)

      for source_path in disk_queue:
        obj_name = self.object_name(source_path)
        try:
          self.log.debug(
              "Uploading '%s' -> '%s' ...",
              source_path,
              obj_name,
              extra={"task": task.id},
          )
          client.upload(source_path, obj_name)
          self.log.debug(
              "Removing '%s' ...",
              source_path,
              extra={"task": task.id},
          )
          os.remove(source_path)
        except self.archival_client_exception_class as exc:
          self.log.error(
              "Failed to upload '%s' ...",
              source_path,
              extra={"task": task.id},
          )
          raise exc
        except OSError as exc:
          self.log.error(
              "Failed to remove '%s' ...",
              source_path,
              extra={"task": task.id},
          )
          raise exc
    return None

  def object_name(self, file_name: str) -> str:
    """Override to derive an object name from the local file name.

    :param file_name: The name of the file being processed.
    :returns: The S3 object name that will be used.
    """

    return os.path.basename(file_name)
