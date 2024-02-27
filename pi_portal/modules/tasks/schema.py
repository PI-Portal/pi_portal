"""Schedulable task schemas."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol, Type, runtime_checkable

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.workers.cron_jobs.bases.cron_job_base import (
      CronJobBase,
  )
  from .enums import RoutingLabel, TaskType
  from .processor.bases.processor_base import TaskProcessorBase
  from .task.bases.task_args_base import TaskArgsBase
  from .task.bases.task_base import TypeGenericTask


@dataclass
class CronModule:
  """A typed representation of a task module."""

  cron_job_class: "Type[CronJobBase[TaskArgsBase]]"


@runtime_checkable
class ProcessorModule(Protocol):
  """A typed representation of a task processor module."""

  ProcessorClass: "Type[TaskProcessorBase[TaskArgsBase, Any]]"


@dataclass
class RegisteredCronJob:
  """A registered task."""

  # pylint: disable=invalid-name
  CronJobClass: "Type[CronJobBase[TaskArgsBase]]"


@dataclass
class RegisteredTask:  # pylint: disable=invalid-name
  """A registered task."""

  ApiEnabled: "bool"
  ArgClass: "Type[TaskArgsBase]"
  TaskClass: "Type[TypeGenericTask]"


@dataclass
class RegisteredProcessor:
  """A typed representation of a registered task processor."""

  # pylint: disable=invalid-name
  ProcessorClass: "Type[TaskProcessorBase[TaskArgsBase, Any]]"


@runtime_checkable
class TaskModule(Protocol):
  """A typed representation of a task module."""

  ApiEnabled: bool
  Args: "Type[TaskArgsBase]"
  ReturnType: Any
  TaskType: "TaskType"
  Task: "Type[TypeGenericTask]"
