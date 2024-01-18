"""Test the TaskRegistry class."""

from typing import Dict
from unittest import mock

from pi_portal.modules.tasks import processor, task
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.workers import cron_jobs
from .. import registry


class TestTaskRegistry:
  """Test the TaskRegistry class."""

  def test_initialize__attributes(
      self,
      task_registry_instance: registry.TaskRegistry,
  ) -> None:
    assert task_registry_instance.processors == {}
    assert task_registry_instance.tasks == {}
    assert task_registry_instance.cron_jobs == []

  def test_filter_tasks__api_enabled__true__returns_correct_tasks(
      self,
      task_registry_instance_with_mocks: registry.TaskRegistry,
      mocked_registered_tasks: "Dict[TaskType, mock.Mock]",
  ) -> None:

    results = task_registry_instance_with_mocks.filter_tasks(api_enabled=True)

    assert results == {
        TaskType.BASE: mocked_registered_tasks[TaskType.BASE],
        TaskType.NON_SCHEDULED: mocked_registered_tasks[TaskType.NON_SCHEDULED],
    }

  def test_filter_tasks__api_disable__false__returns_correct_tasks(
      self,
      task_registry_instance_with_mocks: registry.TaskRegistry,
      mocked_registered_tasks: "Dict[TaskType, mock.Mock]",
  ) -> None:

    results = task_registry_instance_with_mocks.filter_tasks(api_enabled=False)

    assert results == {
        TaskType.QUEUE_MAINTENANCE:
            mocked_registered_tasks[TaskType.QUEUE_MAINTENANCE],
    }

  def test_filter_tasks__api_disable__none__returns_empty_dict(
      self,
      task_registry_instance_with_mocks: registry.TaskRegistry,
  ) -> None:

    results = task_registry_instance_with_mocks.filter_tasks(api_enabled=None)

    assert results == {}

  def test_register__imports_correct_module(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "mock_module"

    task_registry_instance.register_task(mocked_module_name)

    assert mocked_import_module.mock_calls == [
        mock.call(f"{task.__name__}.{mocked_module_name}"),
        mock.call(f"{processor.__name__}.{mocked_module_name}"),
    ]

  def test_register__creates_task(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "mock_module"
    mocked_task_module = mock.Mock()
    mocked_task_module.TaskType = TaskType.BASE
    mocked_import_module.side_effect = [mocked_task_module, mock.Mock()]

    task_registry_instance.register_task(mocked_module_name)

    registered_task = task_registry_instance.tasks[TaskType.BASE]
    assert len(task_registry_instance.tasks) == 1
    assert registered_task.ArgClass == mocked_task_module.Args
    assert registered_task.TaskClass == mocked_task_module.Task

  def test_register__creates_processor(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "mock_module"
    mocked_task_module = mock.Mock()
    mocked_task_module.ProcessorClass.type = TaskType.BASE
    mocked_import_module.side_effect = [mock.Mock(), mocked_task_module]

    task_registry_instance.register_task(mocked_module_name)

    registered_processor = task_registry_instance.processors[TaskType.BASE]
    assert len(task_registry_instance.processors) == 1
    assert registered_processor.ProcessorClass == \
        mocked_task_module.ProcessorClass

  def test_register__non_scheduled__does_not_create_processor(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "non_scheduled"
    mocked_task_module = mock.Mock()
    mocked_task_module.TaskType = TaskType.NON_SCHEDULED
    mocked_import_module.return_value = mocked_task_module

    task_registry_instance.register_task(mocked_module_name)

    assert len(task_registry_instance.tasks) == 1
    assert len(task_registry_instance.processors) == 0

  def test_register_cron_job__imports_correct_module(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "mock_module"

    task_registry_instance.register_cron_job(mocked_module_name)

    mocked_import_module.assert_called_once_with(
        f"{cron_jobs.__name__}.{mocked_module_name}"
    )

  def test_register_cron_job__creates_cron_job(
      self,
      task_registry_instance: registry.TaskRegistry,
      mocked_import_module: mock.Mock,
  ) -> None:
    mocked_module_name = "mock_module"
    mocked_task_module = mock.Mock()
    mocked_import_module.return_value = mocked_task_module

    task_registry_instance.register_cron_job(mocked_module_name)

    created_crpn_job = task_registry_instance.cron_jobs[0]
    assert len(task_registry_instance.cron_jobs) == 1
    assert created_crpn_job.CronJobClass == mocked_task_module.CronJob
