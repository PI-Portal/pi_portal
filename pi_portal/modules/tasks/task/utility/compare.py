"""Test helper to compare tasks and serializers to each other."""

import dataclasses
from typing import Any

from pi_portal.modules.tasks.task.bases import task_args_base, task_result
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from pi_portal.modules.tasks.task.serializers.task_serializer import (
    SerializedTask,
)


def assert_task_equals_serialized_task(
    task: TaskBase[task_args_base.TaskArgsBase, Any],
    serialized_task: SerializedTask,
) -> None:
  """Compare a task to a serialized version of itself.

  :param task: A task instance to compare.
  :param serialized_task: A serialized task to compare.
  """

  for field in dataclasses.fields(serialized_task):
    task_object = getattr(task, field.name)
    serializer_object = getattr(serialized_task, field.name)
    if isinstance(serializer_object, list):
      assert isinstance(task_object, list)
      assert len(task_object) == len(serializer_object)
      # pylint: disable=consider-using-enumerate
      for index in range(0, len(task_object)):
        assert_task_equals_serialized_task(
            task_object[index],
            serializer_object[index],
        )
    elif isinstance(task_object, task_result.TaskResult):
      assert dataclasses.asdict(task_object) == serializer_object
    else:
      assert task_object == serializer_object
