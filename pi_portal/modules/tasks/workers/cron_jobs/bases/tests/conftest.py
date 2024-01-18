"""Fixtures for the cron job modules tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Type
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.task import non_scheduled
from .. import cron_job_base

TypeConcreteJobInstance = cron_job_base.CronJobBase[non_scheduled.Args]


@pytest.fixture
def concrete_cron_job_base_class() -> Type[TypeConcreteJobInstance]:

  class ConcreteCronJob(cron_job_base.CronJobBase[non_scheduled.Args]):
    interval = 10
    type = TaskType.NON_SCHEDULED

    def _args(self) -> non_scheduled.Args:
      return non_scheduled.Args()

  return ConcreteCronJob


@pytest.fixture
def concrete_cron_job_base_instance(
    concrete_cron_job_base_class: Type[TypeConcreteJobInstance],
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> TypeConcreteJobInstance:
  return concrete_cron_job_base_class(
      mocked_worker_logger, mocked_task_registry
  )
