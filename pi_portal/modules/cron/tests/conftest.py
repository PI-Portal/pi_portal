"""Test fixtures for the cron job modules tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import List
from unittest import mock

import pytest
from .. import scheduler


@pytest.fixture
def mocked_cron_jobs() -> List[mock.Mock]:
  return [
      mock.Mock(),
      mock.Mock(),
  ]


@pytest.fixture
def mocked_sys_exit() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def scheduler_instance() -> scheduler.CronScheduler:
  instance = scheduler.CronScheduler()
  return instance


@pytest.fixture
def scheduler_instance_with_mocks(
    mocked_cron_jobs: List[mock.Mock],
    mocked_cron_logger: logging.Logger,
    mocked_sys_exit: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> scheduler.CronScheduler:
  monkeypatch.setattr(scheduler.__name__ + ".sys.exit", mocked_sys_exit)
  instance = scheduler.CronScheduler()
  monkeypatch.setattr(instance, "jobs", mocked_cron_jobs)
  monkeypatch.setattr(instance, "log", mocked_cron_logger)
  return instance
