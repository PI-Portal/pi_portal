"""API models."""

from typing import Any, ClassVar, Dict, List

from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from pi_portal.modules.tasks.registration.registry_factory import (
    RegistryFactory,
)
from pi_portal.modules.tasks.schema import RegisteredTask
from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from pydantic import BaseModel, Field, PrivateAttr, model_validator


class TaskCreationRequestModel(BaseModel):
  """A task creation model for the API."""

  NESTED_FIELDS: ClassVar[List[str]] = ["on_failure", "on_success"]

  _args: "TaskArgsBase" = PrivateAttr()
  _instance: "TaskBase[TaskArgsBase, Any]" = PrivateAttr()
  _registered_tasks: "Dict[TaskType, RegisteredTask]" = PrivateAttr()

  type: "TaskType"
  args: Dict[str, Any]
  on_failure: List["TaskCreationRequestModel"] = []
  on_success: List["TaskCreationRequestModel"] = []
  priority: "TaskPriority" = Field(default=TaskPriority.STANDARD)
  retry_after: int = Field(default=0)

  def model_post_init(self, __context: Any) -> None:
    """Complete model initialization."""
    self._init_registry()

  def _init_registry(self) -> None:
    registry = RegistryFactory().create()
    self._registered_tasks = registry.filter_tasks(api_enabled=True)

  @model_validator(mode='after')
  def validator(self) -> "TaskCreationRequestModel":
    """Validate the model after instantiation."""
    self._validator_type_must_be_valid()
    self._validator_must_instantiate()
    return self

  def _validator_type_must_be_valid(self) -> None:
    if self.type not in self._registered_tasks:
      raise ValueError(
          f"the specified task type is not enabled: {self.type.value}."
      )

  def _validator_must_instantiate(self) -> None:
    try:
      self._instantiate_args()
      self._instantiate_task()
    except TypeError:
      raise ValueError(  # pylint: disable=raise-missing-from
          f"the args provided do not match task type: {self.type.value}."
      )

  def _instantiate_args(self) -> None:
    args_class = self._registered_tasks[self.type].ArgClass
    self._args = args_class(**self.args)

  def _instantiate_task(self) -> None:
    task_class = self._registered_tasks[self.type].TaskClass
    self._instance = task_class(
        args=self._args,
        priority=self.priority,
        retry_after=self.retry_after,
    )

  def as_task(self) -> 'TaskBase[TaskArgsBase, Any]':
    """Return a task instance to represent the work being requested.

    :returns: The created task instance.
    """

    for field_name in self.NESTED_FIELDS:
      task_field_value = getattr(self._instance, field_name, [])
      for model_instance in getattr(self, field_name, []):
        task_field_value.append(model_instance.as_task())
    return self._instance
