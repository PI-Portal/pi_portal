"""Register task and cron job modules."""

from importlib import import_module
from typing import Dict, List, Optional

from pi_portal.modules.tasks import processor, task
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.schema import (
    CronModule,
    ProcessorModule,
    RegisteredCronJob,
    RegisteredProcessor,
    RegisteredTask,
    TaskModule,
)
from pi_portal.modules.tasks.workers import cron_jobs


class TaskRegistry:
  """Tasks registered for use with the scheduler."""

  __slots__ = ("cron_jobs", "processors", "tasks")

  cron_jobs: "List[RegisteredCronJob]"
  processors: "Dict[TaskType, RegisteredProcessor]"
  tasks: "Dict[TaskType, RegisteredTask]"

  def __init__(self) -> None:
    self.cron_jobs = []
    self.processors = {}
    self.tasks = {}

  def filter_tasks(
      self,
      api_enabled: Optional[bool] = None,
  ) -> "Dict[TaskType, RegisteredTask]":
    """Return a filtered list of tasks.

    :param api_enabled: Set to True or False to filter by this value.
    :returns: The filtered dictionary of registered tasks, keyed by task type.
    """
    filtered_results: "Dict[TaskType, RegisteredTask]" = {}
    for task_type, registered_task in self.tasks.items():
      if registered_task.ApiEnabled == api_enabled:
        filtered_results.update({task_type: registered_task})
    return filtered_results

  def register_task(self, module_name: str) -> None:
    """Register the task module and any processor module with this task name.

    :param module_name: The name of the module to register.
    """
    module = self._register_task(module_name)
    if module.TaskType != TaskType.NON_SCHEDULED:
      self._register_processor(module_name)

  def register_cron_job(self, module_name: str) -> None:
    """Register the cron job module with this task name.

    :param module_name: The name of the module to register.
    """
    cron_module = import_module(f"{cron_jobs.__name__}.{module_name}")
    verified_module = CronModule(cron_job_class=getattr(cron_module, "CronJob"))
    self.cron_jobs.append(
        RegisteredCronJob(CronJobClass=verified_module.cron_job_class)
    )

  def _register_task(self, task_module_name: str) -> TaskModule:
    task_module = import_module(f"{task.__name__}.{task_module_name}")

    assert isinstance(task_module, TaskModule)

    registered_task = RegisteredTask(
        ApiEnabled=task_module.ApiEnabled,
        ArgClass=task_module.Args,
        TaskClass=task_module.Task,
    )

    self.tasks.update({
        task_module.TaskType: registered_task,
    })
    return task_module

  def _register_processor(self, processor_module_name: str) -> None:
    processor_module = import_module(
        f"{processor.__name__}.{processor_module_name}"
    )

    assert isinstance(processor_module, ProcessorModule)

    registered_processor = RegisteredProcessor(
        ProcessorClass=processor_module.ProcessorClass
    )
    self.processors.update(
        {
            processor_module.ProcessorClass.type: registered_processor,
        }
    )
