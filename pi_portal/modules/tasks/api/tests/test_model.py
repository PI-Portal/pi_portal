"""Tests for the TaskCreationRequestModel class."""
import os
from copy import deepcopy
from typing import Any, cast

import pytest
from pi_portal import config
from pi_portal.modules.tasks.config import ROUTING_MATRIX
from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
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
      "retry_after":
          3600,
      "routing_label":
          "ARCHIVAL",
      "on_failure":
          [
              {
                  "type": "CHAT_UPLOAD_SNAPSHOT",
                  "args":
                      {
                          "description":
                              "A snapshot for testing purposes.",
                          "path":
                              os.path.join(
                                  config.PATH_MOTION_CONTENT,
                                  "snapshot.jpg",
                              )
                      },
                  "retry_after": 300,
                  "routing_label": "CAMERA",
              }
          ],
      "on_success":
          [
              {
                  "type": "MOTION_SNAPSHOT",
                  "args": {
                      "camera": 2
                  },
                  "retry_after": 0,
                  "routing_label": "CHAT_SEND_MESSAGE",
              }
          ],
  }

  def test_initialize__default_values__attributes(self) -> None:
    instance = JsonInputModelShim(**self.params_with_defaults)

    assert instance.type is TaskType(self.params_with_defaults["type"])
    assert instance.args == self.params_with_defaults["args"]
    assert instance.retry_after == 0
    assert instance.routing_label is ROUTING_MATRIX[instance.type]
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

    assert instance.type is TaskType(self.params_with_nested_values["type"])
    assert instance.args == self.params_with_nested_values["args"]
    assert instance.retry_after is self.params_with_nested_values["retry_after"]
    assert instance.routing_label is RoutingLabel(
        self.params_with_nested_values["routing_label"]
    )
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

    assert instance.type == TaskType(nested_params["type"])
    assert instance.args == nested_params["args"]
    assert instance.retry_after is nested_params["retry_after"]
    assert instance.routing_label == (
        RoutingLabel(nested_params["routing_label"])
    )
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

    assert instance.type is TaskType(nested_params["type"])
    assert instance.args == nested_params["args"]
    assert instance.retry_after is nested_params["retry_after"]
    assert instance.routing_label == (
        RoutingLabel(nested_params["routing_label"])
    )
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

    assert task_instance.type is TaskType(self.params_with_defaults["type"])
    assert task_instance.args.camera == (
        self.params_with_defaults["args"]["camera"]
    )
    assert task_instance.retry_after == 0
    assert task_instance.routing_label == (ROUTING_MATRIX[task_instance.type])
    assert len(task_instance.on_failure) == 0
    assert len(task_instance.on_success) == 0

  def test_as_task__nested_values__attributes__base(self) -> None:
    task_instance = (
        JsonInputModelShim(**self.params_with_nested_values).as_task()
    )

    assert isinstance(task_instance, motion_snapshot.Task)
    assert isinstance(task_instance.args, motion_snapshot.Args)

    assert task_instance.type is TaskType(
        self.params_with_nested_values["type"]
    )
    assert task_instance.args.camera == (
        self.params_with_nested_values["args"]["camera"]
    )
    assert task_instance.retry_after is (
        self.params_with_nested_values["retry_after"]
    )
    assert task_instance.routing_label == (
        RoutingLabel(self.params_with_nested_values["routing_label"])
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

    assert nested_instance.type is TaskType(nested_params["type"])
    assert nested_instance.args.path == nested_params["args"]["path"]
    assert nested_instance.retry_after is nested_params["retry_after"]
    assert nested_instance.routing_label == (
        RoutingLabel(nested_params["routing_label"])
    )
    assert len(nested_instance.on_failure) == 0
    assert len(nested_instance.on_failure) == 0

  def test_as_task__nested_values__attributes__on_success(self) -> None:
    nested_params = self.params_with_nested_values["on_success"][0]

    nested_instance = \
        JsonInputModelShim(**self.params_with_nested_values). \
        on_success[0].as_task()

    assert isinstance(nested_instance, motion_snapshot.Task)
    assert isinstance(nested_instance.args, motion_snapshot.Args)

    assert nested_instance.type is TaskType(nested_params["type"])
    assert nested_instance.args.camera == nested_params["args"]["camera"]
    assert nested_instance.retry_after is nested_params["retry_after"]
    assert nested_instance.routing_label == (
        RoutingLabel(nested_params["routing_label"])
    )
    assert len(nested_instance.on_failure) == 0
    assert len(nested_instance.on_failure) == 0
