"""Processes requests to manage a supervisor process."""
from typing import Callable, Dict

from pi_portal.modules.system.supervisor_config import ProcessStatus
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcess,
    SupervisorProcessException,
)
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import supervisor_process


class ProcessorClass(
    processor_base.TaskProcessorBase[
        supervisor_process.Args,
        supervisor_process.ReturnType,
    ],
):
  """Processes requests to manage a supervisor process."""

  __slots__ = ()

  type = TaskType.SUPERVISOR_PROCESS

  def _process(
      self,
      task: processor_base.TaskBase[
          supervisor_process.Args,
          supervisor_process.ReturnType,
      ],
  ) -> supervisor_process.ReturnType:

    managed_process = SupervisorProcess(task.args.process)

    self.log.info(
        "Supervisord process management request: '%s' -> '%s' ...",
        task.args.process.value,
        task.args.requested_state.value,
        extra={
            "task_id": task.id,
            "task_type": task.type.value,
        },
    )

    method: Dict[ProcessStatus, Callable[[], None]] = {
        ProcessStatus.STOPPED: managed_process.stop,
        ProcessStatus.RUNNING: managed_process.start,
    }

    try:
      method[task.args.requested_state]()
    except SupervisorProcessException:
      self.log.info(
          "Supervisord process already in requested state: '%s' -> '%s' !",
          task.args.process.value,
          task.args.requested_state.value,
          extra={
              "task_id": task.id,
              "task_type": task.type.value,
          },
      )
