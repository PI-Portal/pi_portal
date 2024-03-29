"""The persist-queue library's implementation of a queue."""
import logging
import os
import shutil
from typing import TYPE_CHECKING, Optional, cast

from persistqueue import Empty as VendorException
from persistqueue import SQLiteAckQueue as VendorQueue
from pi_portal import config
from typing_extensions import TypedDict
from .bases.queue_base import QueueBase, QueueMetrics

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import RoutingLabel
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class TypeRawTask(TypedDict):
  """Typed representation of a 'raw' deserialized persist-queue task."""

  pqid: int
  data: "TypeGenericTask"


class Queue(QueueBase):
  """The persist-queue library's implementation of a queue.

  :param log:  A logger instance.
  """

  __slots__ = ("_path", "_queue")

  _active_size = 0
  _db_path = config.PATH_TASKS_SERVICE_DATABASES
  _queue: VendorQueue
  timeout = 2

  def __init__(
      self,
      log: logging.Logger,
      routing_label: "RoutingLabel",
  ) -> None:
    super().__init__(log, routing_label)
    self._path = os.path.join(self._db_path, routing_label.value)
    self._initialize()

  def _initialize(self) -> None:
    os.makedirs(self._path, exist_ok=True)
    self._queue = VendorQueue(
        path=self._path,
        auto_resume=True,
        multithreading=True,
        timeout=self.timeout,
    )

  def raw(self) -> VendorQueue:
    """Access the underlying queue directly."""

    return self._queue

  def _ack(self, task: "TypeGenericTask") -> None:
    self._queue.ack(id=task.id)

  def _get(self) -> "TypeGenericTask":
    try:
      raw_data = self._responsive_get()
      item = raw_data['data']
      item.id = raw_data['pqid']
      return item
    except AttributeError:
      self.log.error(
          "Fatal error during deserialization!",
          extra={
              "task": None,
              'queue': self.routing_label.value
          },
      )
      self.log.error(
          "To restore service the queue is being cleared. "
          "Tasks have been lost!",
          extra={
              "task": None,
              'queue': self.routing_label.value
          },
      )
      shutil.rmtree(self._path)
      self._initialize()
      return self._get()

  def _responsive_get(self) -> "TypeRawTask":
    raw_data: "Optional[TypeRawTask]" = None

    while not raw_data:
      try:
        raw_data = cast(
            TypeRawTask,
            self._queue.get(block=True, timeout=1, raw=True),
        )
      except VendorException:
        pass

    return raw_data

  def _maintenance(self) -> None:
    self._queue.clear_acked_data()
    self._queue.shrink_disk_usage()

  def _metrics(self) -> "QueueMetrics":
    return QueueMetrics(
        length=self._queue.size,
        acked_length=self._queue.acked_count(),
        unacked_length=self._queue.unack_count(),
        storage=self._size_on_disk_in_mb()
    )

  def _size_on_disk_in_mb(self) -> float:
    return sum(
        os.path.getsize(f) for f in os.scandir(self._path) if f.is_file()
    ) / 1024 / 1024

  def _put(self, task: "TypeGenericTask") -> None:
    task.id = self._queue.put(task)

  def _retry(self, task: "TypeGenericTask") -> None:
    self._queue.nack(id=task.id)
