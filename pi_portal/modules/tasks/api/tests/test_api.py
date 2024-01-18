"""Test the API."""

from dataclasses import asdict
from unittest import mock

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from pi_portal.modules.tasks.registration.registry import TaskRegistry
from pi_portal.modules.tasks.task.serializers.task_serializer import (
    SerializedTask,
)
from .conftest import (
    TypedTaskCreationRequestParameters,
    disabled_tasks__valid_payloads__creation_request_scenarios,
    enabled_tasks__invalid__payloads__creation_request_scenarios,
    enabled_tasks__valid_payloads__creation_request_scenarios,
)


class TestApi:
  """Test the API."""

  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__enabled__valid_payload__vary_task__returns_200(
      self,
      test_client: TestClient,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    response = test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    assert response.status_code == 200

  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__enabled__valid_payload__vary_task__returns_serialized_task(
      self,
      mocked_task_router: mock.Mock,
      test_client: TestClient,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    response = test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    created_task = mocked_task_router.return_value.mock_calls[0].args[0]
    assert response.json() == \
           jsonable_encoder(SerializedTask.serialize(created_task))

  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__enabled__valid_payload__vary_task__def_priority__enqueues(
      self,
      test_client: TestClient,
      mocked_task_router: mock.Mock,
      task_registry: TaskRegistry,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    mocked_task_router.return_value.put.assert_called_once()
    created_task = mocked_task_router.return_value.mock_calls[0].args[0]
    registered_task = task_registry.tasks[TaskType(request_scenario["type"])]
    assert isinstance(
        created_task,
        registered_task.TaskClass,
    )
    assert isinstance(
        created_task.args,
        registered_task.ArgClass,
    )
    assert asdict(created_task.args) == request_scenario["args"]
    assert created_task.priority == TaskPriority.STANDARD

  @pytest.mark.parametrize("priority", list(TaskPriority))
  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__enabled__valid_payload__vary_task__vary_priority__enqueues(
      self,
      test_client: TestClient,
      mocked_task_router: mock.Mock,
      task_registry: TaskRegistry,
      request_scenario: TypedTaskCreationRequestParameters,
      priority: TaskPriority,
  ) -> None:
    request_scenario["priority"] = priority.value

    test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    mocked_task_router.return_value.put.assert_called_once()
    created_task = mocked_task_router.return_value.mock_calls[0].args[0]
    registered_task = task_registry.tasks[TaskType(request_scenario["type"])]
    assert isinstance(
        created_task,
        registered_task.TaskClass,
    )
    assert isinstance(
        created_task.args,
        registered_task.ArgClass,
    )
    assert asdict(created_task.args) == request_scenario["args"]
    assert created_task.priority == priority

  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__invalid__payloads__creation_request_scenarios,
  )
  def test_request__enabled__invalid_payload__vary_task__returns_422(
      self,
      test_client: TestClient,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    response = test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    assert response.status_code == 422

  @pytest.mark.parametrize(
      "request_scenario",
      enabled_tasks__invalid__payloads__creation_request_scenarios,
  )
  def test_request__enabled__invalid_payload__vary_task__does_not_enqueue(
      self,
      test_client: TestClient,
      mocked_task_router: mock.Mock,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    mocked_task_router.return_value.put.assert_not_called()

  @pytest.mark.parametrize(
      "request_scenario",
      disabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__disabled__valid_payload__vary_task__returns_422(
      self,
      test_client: TestClient,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    response = test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    assert response.status_code == 422

  @pytest.mark.parametrize(
      "request_scenario",
      disabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__disabled__valid_payload__vary_task__returns_error_message(
      self,
      test_client: TestClient,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    response = test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    assert response.json()["detail"][0]["msg"] == (
        "Value error, the specified task type is not enabled: "
        f"{request_scenario['type']}."
    )

  @pytest.mark.parametrize(
      "request_scenario",
      disabled_tasks__valid_payloads__creation_request_scenarios,
  )
  def test_request__disabled__valid_payload__vary_task__does_not_enqueue(
      self,
      test_client: TestClient,
      mocked_task_router: mock.Mock,
      request_scenario: TypedTaskCreationRequestParameters,
  ) -> None:
    test_client.post(
        "/schedule/",
        json=request_scenario,
    )

    mocked_task_router.return_value.put.assert_not_called()
