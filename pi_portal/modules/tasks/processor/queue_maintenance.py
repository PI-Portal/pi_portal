"""Processes requests to perform maintenance on the queue."""
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.queue import TaskRouter
from pi_portal.modules.tasks.task import queue_maintenance


class ProcessorClass(
    processor_base.TaskProcessorBase[
        queue_maintenance.Args,
        queue_maintenance.ReturnType,
    ],
):
  """Processes requests to perform maintenance on the queue."""

  __slots__ = ()

  type = TaskType.QUEUE_MAINTENANCE

  def _process(
      self,
      task: processor_base.TaskBase[
          queue_maintenance.Args,
          queue_maintenance.ReturnType,
      ],
  ) -> queue_maintenance.ReturnType:
    router = TaskRouter(self.log)
    for routing_label, queue in router.queues.items():
      self.log.warning(
          "Performing maintenance on the '%s' task queue ...",
          routing_label.value,
          extra={
              "task": task.id,
              "queue": routing_label.value
          },
      )
      queue.maintenance()
