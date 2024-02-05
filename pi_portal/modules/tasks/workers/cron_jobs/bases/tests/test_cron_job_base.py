"""Test the CronJobBase class."""
import logging
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from .. import cron_job_base
from .conftest import TypeConcreteJobInstance


class TestCronJobBase:
  """Test the CronJobBase class."""

  def test_initialize__attributes(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_task_registry: mock.Mock,
  ) -> None:
    assert concrete_cron_job_base_instance.interval == 10
    assert concrete_cron_job_base_instance.time_remaining == \
           concrete_cron_job_base_instance.interval
    assert concrete_cron_job_base_instance.type == \
        TaskType.NON_SCHEDULED
    assert concrete_cron_job_base_instance.\
        registered_task.TaskClass == \
        mocked_task_registry.tasks[TaskType.NON_SCHEDULED].TaskClass
    assert concrete_cron_job_base_instance.retry_after == 0

  def test_initialize__logging(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_worker_logger: logging.Logger,
  ) -> None:
    assert concrete_cron_job_base_instance.log == \
           mocked_worker_logger
    assert isinstance(
        concrete_cron_job_base_instance.log,
        logging.Logger,
    )

  def test_initialize__inheritance(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
  ) -> None:
    assert isinstance(
        concrete_cron_job_base_instance,
        cron_job_base.CronJobBase,
    )

  def test_schedule__resets_elapsed(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_task_router: mock.Mock,
  ) -> None:
    concrete_cron_job_base_instance.time_remaining = 1

    concrete_cron_job_base_instance.schedule(mocked_task_router)

    assert concrete_cron_job_base_instance.time_remaining == \
           concrete_cron_job_base_instance.interval

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_schedule__vary_priority__creates_correct_task(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_task_router: mock.Mock,
      mocked_task_registry: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
      priority: TaskPriority,
  ) -> None:
    monkeypatch.setattr(
        concrete_cron_job_base_instance,
        "priority",
        priority,
    )

    concrete_cron_job_base_instance.schedule(mocked_task_router)

    mocked_task_registry.tasks[concrete_cron_job_base_instance.type].\
        TaskClass.assert_called_once_with(
            # pylint: disable=protected-access
            args=concrete_cron_job_base_instance._args(),
            priority=priority,
            retry_after=concrete_cron_job_base_instance.retry_after,
        )

  @pytest.mark.parametrize("retry_after", [-1, 0, 10])
  def test_schedule__vary_retry_after__creates_correct_task(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_task_router: mock.Mock,
      mocked_task_registry: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
      retry_after: int,
  ) -> None:
    monkeypatch.setattr(
        concrete_cron_job_base_instance,
        "retry_after",
        retry_after,
    )

    concrete_cron_job_base_instance.schedule(mocked_task_router)

    mocked_task_registry.tasks[concrete_cron_job_base_instance.type]. \
        TaskClass.assert_called_once_with(
        # pylint: disable=protected-access
        args=concrete_cron_job_base_instance._args(),
        priority=concrete_cron_job_base_instance.priority,
        retry_after=retry_after,
      )

  def test_schedule__adds_task_to_queue(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
      mocked_task_router: mock.Mock,
      mocked_task_registry: mock.Mock,
  ) -> None:
    concrete_cron_job_base_instance.schedule(mocked_task_router)

    assert mocked_task_router.put.call_count == 1
    assert len(mocked_task_router.put.call_args_list) == 1
    task = mocked_task_router.put.call_args_list[0].args[0]
    assert task == (
        mocked_task_registry.tasks[concrete_cron_job_base_instance.type
                                  ].TaskClass.return_value
    )

  def test_tick__decrements_elapsed(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
  ) -> None:
    concrete_cron_job_base_instance.time_remaining = 5

    concrete_cron_job_base_instance.tick()
    concrete_cron_job_base_instance.tick()

    assert concrete_cron_job_base_instance.time_remaining == 5 - 2

  def test_tick__when_elapsed_is_below_1__raises_correct_exception(
      self,
      concrete_cron_job_base_instance: TypeConcreteJobInstance,
  ) -> None:
    concrete_cron_job_base_instance.time_remaining = 2

    with pytest.raises(cron_job_base.CronJobAlarm):
      concrete_cron_job_base_instance.tick()
      concrete_cron_job_base_instance.tick()
