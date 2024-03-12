"""Test fixtures for the cron job mixins classes."""
# pylint: disable=redefined-outer-name

import logging
from typing import Type

import pytest
from .. import metrics_logger


@pytest.fixture
def concrete_metrics_cron_job() -> Type[metrics_logger.MetricsLoggerMixin]:

  class ConcreteCronJob(metrics_logger.MetricsLoggerMixin):
    pass

  return ConcreteCronJob


@pytest.fixture
def concrete_metrics_cron_job_instance(
    concrete_metrics_cron_job: Type[metrics_logger.MetricsLoggerMixin],
) -> metrics_logger.MetricsLoggerMixin:

  return concrete_metrics_cron_job()


@pytest.fixture
def metrics_logger_instance(
    mocked_metrics_logger: logging.Logger,
) -> metrics_logger.MetricsLogger:
  instance = metrics_logger.MetricsLogger()
  setattr(
      instance,
      "log",
      mocked_metrics_logger,
  )
  return instance
