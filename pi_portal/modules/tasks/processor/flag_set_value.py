"""Processes requests to set a flag's value."""

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.flags import FlagState
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import flag_set_value


class ProcessorClass(
    processor_base.TaskProcessorBase[
        flag_set_value.Args,
        flag_set_value.ReturnType,
    ],
):
  """Processes requests to set a flag's value."""

  __slots__ = ()

  type = TaskType.FLAG_SET_VALUE

  def _process(
      self,
      task: processor_base.TaskBase[
          flag_set_value.Args,
          flag_set_value.ReturnType,
      ],
  ) -> flag_set_value.ReturnType:

    self.log.debug(
        "Setting flag: '%s' -> '%s' .",
        task.args.flag_name,
        task.args.value,
        extra={
            "task_id": task.id,
            "task_type": task.type.value,
        },
    )

    setattr(
        FlagState().flags,
        task.args.flag_name,
        task.args.value,
    )
