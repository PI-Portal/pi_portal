"""Tests for the TaskCreationRequestModel class."""
from copy import deepcopy
from typing import Any, cast

import pytest
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from pi_portal.modules.tasks.task import chat_upload_snapshot, motion_snapshot
from typing_extensions import Unpack
from .. import model
from .conftest import TypedTaskCreationRequestParameters


class JsonInputModelShim(model.TaskCreationRequestModel):
  """Performs type conversion to allow testing the model with request JSON."""

  def __init__(
      self,
      **data: Unpack[TypedTaskCreationRequestParameters],
  ) -> None:
    super().__init__(**cast(Any, data))


class TestTaskCreationRequestModel:
  """Tests for the TaskCreationRequestModel class."""

  params_with_defaults: TypedTaskCreationRequestParameters = {
      "type": "MOTION_SNAPSHOT",
      "args": {
          "camera": 1
      },
  }

  params_with_disabled_task: TypedTaskCreationRequestParameters = {
      "type": "NON_SCHEDULED",
      "args": {},
  }

  params_with_nested_values: TypedTaskCreationRequestParameters = {
      "type":
          "MOTION_SNAPSHOT",
      "args": {
          "camera": 1
      },
      "priority":
          "EXPRESS",
      "retry_on_error":
          True,
      "on_failure":
          [
              {
                  "type": "CHAT_UPLOAD_SNAPSHOT",
                  "args": {
                      "path": "/var/lib/snapshot.jpg"
                  },
                  "priority": "STANDARD",
                  "retry_on_error": True,
              }
          ],
      "on_success":
          [
              {
                  "type": "MOTION_SNAPSHOT",
                  "args": {
                      "camera": 2
                  },
                  "priority": "EXPRESS",
                  "retry_on_error": False,
              }
          ],
  }

  def test_initialize__default_values__attributes(self) -> None:
    instance = JsonInputModelShim(**self.params_with_defaults)

    assert instance.priority is TaskPriority.STANDARD
    assert instance.type is TaskType(self.params_with_defaults["type"])
    assert instance.args == self.params_with_defaults["args"]
    assert instance.retry_on_error is False
    assert len(instance.on_failure) == 0
    assert len(instance.on_success) == 0

  def test_initialize__default_values__invalid_args(self) -> None:
    invalid_default_value_params = deepcopy(self.params_with_defaults)
    invalid_default_value_params["args"] = {"mock_args": "mock_value"}

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**invalid_default_value_params)

    assert str(exc.value).splitlines()[1].startswith(
        "  Value error, the args provided do not match task type: "
        "MOTION_SNAPSHOT."
    )

  def test_initialize__default_values__disabled_task(self) -> None:
    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**self.params_with_disabled_task)

    assert str(exc.value).splitlines()[1].startswith(
        "  Value error, the specified task type is not enabled: "
        "NON_SCHEDULED."
    )

  def test_initialize__nested_values__attributes__valid_base_args(self) -> None:
    instance = JsonInputModelShim(**self.params_with_nested_values)

    assert instance.priority is TaskPriority(
        self.params_with_nested_values["priority"]
    )
    assert instance.type is TaskType(self.params_with_nested_values["type"])
    assert instance.args == self.params_with_nested_values["args"]
    assert instance.retry_on_error is self.params_with_nested_values[
        "retry_on_error"]
    assert len(instance.on_failure) == 1
    assert len(instance.on_failure) == 1

  def test_initialize__nested_values__attributes__invalid_base_args(
      self
  ) -> None:
    invalid_base_params = deepcopy(self.params_with_nested_values)
    invalid_base_params.update({"args": {"mock_args": "mock_value"}})

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**invalid_base_params)

    assert str(exc.value).splitlines()[1].startswith(
        "  Value error, the args provided do not match task type: "
        "MOTION_SNAPSHOT."
    )

  def test_initialize__nested_values__attributes__disabled_base_task_type(
      self
  ) -> None:
    disabled_task_base_params = deepcopy(self.params_with_nested_values)
    disabled_task_base_params["type"] = "NON_SCHEDULED"

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**disabled_task_base_params)

    assert str(exc.value).splitlines()[1].startswith(
        "  Value error, the specified task type is not enabled: "
        "NON_SCHEDULED."
    )

  def test_initialize__nested_values__attributes__valid_on_failure_args(
      self
  ) -> None:
    nested_params = self.params_with_nested_values["on_failure"][0]

    instance = JsonInputModelShim(**self.params_with_nested_values).\
        on_failure[0]

    assert instance.priority is TaskPriority(nested_params["priority"])
    assert instance.type is TaskType(nested_params["type"])
    assert instance.args == nested_params["args"]
    assert instance.retry_on_error is nested_params["retry_on_error"]
    assert len(instance.on_failure) == 0
    assert len(instance.on_failure) == 0

  def test_initialize__nested_values__attributes__invalid_on_failure_args(
      self
  ) -> None:
    invalid_nested_params = deepcopy(self.params_with_nested_values)
    invalid_nested_params["on_failure"][0]["args"] = {"mock_arg": "mock_value"}

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**invalid_nested_params)

    assert str(exc.value).splitlines()[2].startswith(
        "  Value error, the args provided do not match task type: "
        "CHAT_UPLOAD_SNAPSHOT"
    )

  def test_initialize__nested_values__attributes__disabled_on_failure_task_type(
      self
  ) -> None:
    disabled_task_nested_params = deepcopy(self.params_with_nested_values)
    disabled_task_nested_params["on_failure"][0]["type"] = "NON_SCHEDULED"

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**disabled_task_nested_params)

    assert str(exc.value).splitlines()[2].startswith(
        "  Value error, the specified task type is not enabled: "
        "NON_SCHEDULED."
    )

  def test_initialize__nested_values__attributes__valid_on_success_args(
      self
  ) -> None:
    nested_params = self.params_with_nested_values["on_success"][0]

    instance = JsonInputModelShim(**self.params_with_nested_values).\
        on_success[0]

    assert instance.priority is TaskPriority(nested_params["priority"])
    assert instance.type is TaskType(nested_params["type"])
    assert instance.args == nested_params["args"]
    assert instance.retry_on_error is nested_params["retry_on_error"]
    assert len(instance.on_failure) == 0
    assert len(instance.on_failure) == 0

  def test_initialize__nested_values__attributes__invalid_on_success_args(
      self
  ) -> None:
    invalid_nested_params = deepcopy(self.params_with_nested_values)
    invalid_nested_params["on_success"][0]["args"] = {"mock_arg": "mock_value"}

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**invalid_nested_params)

    assert str(exc.value).splitlines()[2].startswith(
        "  Value error, the args provided do not match task type: "
        "MOTION_SNAPSHOT."
    )

  def test_initialize__nested_values__attributes__disabled_on_success_task_type(
      self
  ) -> None:
    disabled_task_nested_params = deepcopy(self.params_with_nested_values)
    disabled_task_nested_params["on_success"][0]["type"] = "NON_SCHEDULED"

    with pytest.raises(ValueError) as exc:
      JsonInputModelShim(**disabled_task_nested_params)

    assert str(exc.value).splitlines()[2].startswith(
        "  Value error, the specified task type is not enabled: "
        "NON_SCHEDULED."
    )

  def test_as_task__default_values__attributes(self) -> None:
    task_instance = JsonInputModelShim(**self.params_with_defaults).as_task()

    assert isinstance(task_instance, motion_snapshot.Task)
    assert isinstance(task_instance.args, motion_snapshot.Args)

    assert task_instance.priority is TaskPriority.STANDARD
    assert task_instance.type is TaskType(self.params_with_defaults["type"])
    assert task_instance.args.camera == (
        self.params_with_defaults["args"]["camera"]
    )
    assert task_instance.retry_on_error is False
    assert len(task_instance.on_failure) == 0
    assert len(task_instance.on_success) == 0

  def test_as_task__nested_values__attributes__base(self) -> None:
    task_instance = (
        JsonInputModelShim(**self.params_with_nested_values).as_task()
    )

    assert isinstance(task_instance, motion_snapshot.Task)
    assert isinstance(task_instance.args, motion_snapshot.Args)

    assert task_instance.priority is TaskPriority(
        self.params_with_nested_values["priority"]
    )
    assert task_instance.type is TaskType(
        self.params_with_nested_values["type"]
    )
    assert task_instance.args.camera == (
        self.params_with_nested_values["args"]["camera"]
    )
    assert task_instance.retry_on_error is (
        self.params_with_nested_values["retry_on_error"]
    )
    assert len(task_instance.on_failure) == 1
    assert len(task_instance.on_failure) == 1

  def test_as_task__nested_values__attributes__on_failure(self) -> None:
    nested_params = self.params_with_nested_values["on_failure"][0]

    nested_instance = \
        JsonInputModelShim(**self.params_with_nested_values). \
        on_failure[0].as_task()

    assert isinstance(nested_instance, chat_upload_snapshot.Task)
    assert isinstance(nested_instance.args, chat_upload_snapshot.Args)

    assert nested_instance.priority is TaskPriority(nested_params["priority"])
    assert nested_instance.type is TaskType(nested_params["type"])
    assert nested_instance.args.path == nested_params["args"]["path"]
    assert nested_instance.retry_on_error is nested_params["retry_on_error"]
    assert len(nested_instance.on_failure) == 0
    assert len(nested_instance.on_failure) == 0

  def test_as_task__nested_values__attributes__on_success(self) -> None:
    nested_params = self.params_with_nested_values["on_success"][0]

    nested_instance = \
        JsonInputModelShim(**self.params_with_nested_values). \
        on_success[0].as_task()

    assert isinstance(nested_instance, motion_snapshot.Task)
    assert isinstance(nested_instance.args, motion_snapshot.Args)

    assert nested_instance.priority is TaskPriority(nested_params["priority"])
    assert nested_instance.type is TaskType(nested_params["type"])
    assert nested_instance.args.camera == nested_params["args"]["camera"]
    assert nested_instance.retry_on_error is nested_params["retry_on_error"]
    assert len(nested_instance.on_failure) == 0
    assert len(nested_instance.on_failure) == 0
