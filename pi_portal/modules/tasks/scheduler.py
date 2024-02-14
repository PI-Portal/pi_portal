"""TaskScheduler class."""

from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Dict, List

from pi_portal import config
from pi_portal.modules.mixins import write_archived_log_file
from pi_portal.modules.tasks.manifest import TaskManifestFactory
from pi_portal.modules.tasks.workers.cron_worker import CronWorker
from pi_portal.modules.tasks.workers.failed_task_worker import FailedTaskWorker
from pi_portal.modules.tasks.workers.queue_worker import QueueWorker
from .config import QUEUE_WORKER_CONFIGURATION
from .enums import TaskManifests, TaskType
from .queue import TaskRouter
from .registration.registry_factory import RegistryFactory

if TYPE_CHECKING:  # pragma: no cover
  from concurrent.futures import Future

  from pi_portal.modules.tasks.manifest.bases.task_manifest_base import (
      TaskManifestBase,
  )
  from pi_portal.modules.tasks.workers.bases.worker_base import WorkerBase
  from .enums import TaskPriority


class TaskScheduler(write_archived_log_file.ArchivedLogFileWriter):
  """Threaded task scheduler."""

  __slots__ = ("manifests", "registry", "router", "managed_workers")

  logger_name = "tasks"
  log_file_path = config.LOG_FILE_TASK_SCHEDULER

  def __init__(self) -> None:
    self.configure_logger()
    self.registry = RegistryFactory().create()
    self.router = TaskRouter(self.log)
    self.managed_workers: List["WorkerBase"] = []
    self.manifests: "Dict[TaskManifests, TaskManifestBase]" = {}

  def start(self) -> None:
    """Start a pool of worker threads."""

    threads: "List[Future[None]]" = []

    self.log.warning("Task scheduler is starting ...",)

    self._create_manifest(TaskManifests.FAILED_TASKS)

    self._create_cron_worker()
    self._create_failed_task_worker()
    for priority, count in QUEUE_WORKER_CONFIGURATION.items():
      self._create_queue_worker_pool(count, priority)

    with ThreadPoolExecutor(max_workers=len(self.managed_workers)) as executor:
      for worker in self.managed_workers:
        threads.append(executor.submit(worker.start))

    for thread in threads:
      thread.result()

  def _create_manifest(self, manifest: TaskManifests) -> None:
    self.log.warning(
        "Creating the '%s' manifest ...",
        manifest.value,
    )
    self.manifests[manifest] = TaskManifestFactory.create(manifest)

  def _create_cron_worker(self) -> None:
    self.log.warning(
        "Creating the cron scheduler ...", extra={"cron": "scheduler"}
    )
    self.managed_workers.append(
        CronWorker(self.log, self.router, self.registry)
    )

  def _create_failed_task_worker(self) -> None:
    self.log.warning("Creating the failed task scheduler ...")
    self.managed_workers.append(
        FailedTaskWorker(
            self.log,
            self.router,
            self.manifests[TaskManifests.FAILED_TASKS],
        )
    )

  def _create_queue_worker_pool(
      self, count: int, priority: "TaskPriority"
  ) -> None:
    self.log.warning(
        "Creating the '%s' queue worker pool ...",
        priority.value,
        extra={"queue": priority.value}
    )
    for _ in range(0, count):
      self.managed_workers.append(self._create_queue_worker(priority))

  def _create_queue_worker(self, priority: "TaskPriority") -> QueueWorker:
    return QueueWorker(
        self.log,
        self.router.queues[priority],
        self.registry,
        self.manifests[TaskManifests.FAILED_TASKS],
    )

  def halt(self) -> None:
    """Gracefully shutdown the scheduler."""

    for worker in self.managed_workers:
      worker.halt()

    self._do_unblock_workers()

    for manifest in self.manifests.values():
      manifest.close()

    self.log.warning("Task scheduler is shutting down ...",)

  def _do_unblock_workers(self) -> None:
    task_class = self.registry.tasks[TaskType.NON_SCHEDULED].TaskClass
    arg_class = self.registry.tasks[TaskType.NON_SCHEDULED].ArgClass

    for priority, count in QUEUE_WORKER_CONFIGURATION.items():
      for _ in range(0, count):
        task = task_class(args=arg_class(), priority=priority)
        self.router.put(task)
