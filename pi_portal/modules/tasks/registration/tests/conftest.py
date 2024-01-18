"""Test fixtures for the task resignation modules tests."""
# pylint: disable=redefined-outer-name

from typing import Dict
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from .. import registry, registry_factory


@pytest.fixture
def mocked_import_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_registered_tasks() -> "Dict[TaskType, mock.Mock]":
  mock1, mock2, mock3 = mock.Mock(), mock.Mock(), mock.Mock()
  mock1.ApiEnabled, mock2.ApiEnabled = True, True
  mock3.ApiEnabled = False
  return {
      TaskType.BASE: mock1,
      TaskType.NON_SCHEDULED: mock2,
      TaskType.QUEUE_MAINTENANCE: mock3,
  }


@pytest.fixture
def mocked_task_registry() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def task_registry_instance(
    mocked_import_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> registry.TaskRegistry:
  monkeypatch.setattr(
      registry.__name__ + ".import_module",
      mocked_import_module,
  )
  instance = registry.TaskRegistry()
  return instance


@pytest.fixture
def task_registry_instance_with_mocks(
    mocked_import_module: mock.Mock,
    mocked_registered_tasks: "Dict[TaskType, mock.Mock]",
    monkeypatch: pytest.MonkeyPatch,
) -> registry.TaskRegistry:
  monkeypatch.setattr(
      registry.__name__ + ".import_module",
      mocked_import_module,
  )
  instance = registry.TaskRegistry()
  monkeypatch.setattr(instance, "tasks", mocked_registered_tasks)
  return instance


@pytest.fixture
def task_registry_factory_instance(
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> registry_factory.RegistryFactory:
  monkeypatch.setattr(
      registry_factory.__name__ + ".TaskRegistry",
      mocked_task_registry,
  )
  instance = registry_factory.RegistryFactory()
  # pylint: disable=protected-access
  registry_factory.RegistryFactory._registry = None
  return instance


@pytest.fixture
def task_registry_factory_instance_clone(
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> registry_factory.RegistryFactory:
  monkeypatch.setattr(
      registry_factory.__name__ + ".TaskRegistry",
      mocked_task_registry,
  )
  instance = registry_factory.RegistryFactory()
  return instance
