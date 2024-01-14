"""Test the CronScheduler class."""
import logging
from io import StringIO
from types import TracebackType
from typing import List, Optional
from unittest import mock

from pi_portal import config
from .. import scheduler
from ..jobs import cron_jobs


class MockedTraceableException(Exception):

  @property
  def __traceback__(self) -> Optional[TracebackType]:  # type: ignore[override]
    return None


class TestCronScheduler:
  """Test the CronScheduler class."""

  def test__initialization__attrs(
      self,
      scheduler_instance: scheduler.CronScheduler,
  ) -> None:
    assert scheduler_instance.jobs == cron_jobs
    assert scheduler_instance.log_file_path == config.LOG_FILE_CRON_SCHEDULER
    assert scheduler_instance.logger_name == "cron"
    assert scheduler_instance.name == "scheduler"
    assert isinstance(
        scheduler_instance.log,
        logging.Logger,
    )

  def test__start__normal_start_up__logging(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    scheduler_instance_with_mocks.start()

    assert mocked_cron_logger_stream.getvalue() == \
        "WARNING - scheduler - Cron scheduler is starting ...\n"

  def test__start__normal_start_up__job_calls(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_cron_jobs: List[mock.Mock],
  ) -> None:
    scheduler_instance_with_mocks.start()

    for job in mocked_cron_jobs:
      job.assert_called_once_with(scheduler_instance_with_mocks.log)
      job.return_value.start.assert_called_once_with()

  def test__start__normal_start_up__sys_exit(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_sys_exit: mock.Mock,
  ) -> None:
    scheduler_instance_with_mocks.start()

    mocked_sys_exit.assert_not_called()

  def test__start__exception__logging(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_cron_jobs: List[mock.Mock],
      mocked_cron_logger_stream: StringIO,
  ) -> None:

    mocked_cron_jobs[0].return_value.start.side_effect = \
        MockedTraceableException
    mocked_cron_job_name = mocked_cron_jobs[0].name

    scheduler_instance_with_mocks.start()

    assert mocked_cron_logger_stream.getvalue() == (
        "WARNING - scheduler - Cron scheduler is starting ...\n"
        f"ERROR - scheduler - Job '{mocked_cron_job_name}' has failed!\n"
        f"ERROR - {mocked_cron_job_name} - Exception\n"
        "pi_portal.modules.cron.tests.scheduler_test.MockedTraceableException\n"
        "ERROR - scheduler - Cron scheduler is now terminating ...\n"
    )

  def test__start__exception__job_calls(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_cron_jobs: List[mock.Mock],
  ) -> None:
    mocked_cron_jobs[0].return_value.start.side_effect = \
        MockedTraceableException

    scheduler_instance_with_mocks.start()

    for job in mocked_cron_jobs:
      job.assert_called_once_with(scheduler_instance_with_mocks.log)
      job.return_value.start.assert_called_once_with()

  def test__start__exception__sys_exit_call(
      self,
      scheduler_instance_with_mocks: scheduler.CronScheduler,
      mocked_cron_jobs: List[mock.Mock],
      mocked_sys_exit: mock.Mock,
  ) -> None:
    mocked_cron_jobs[0].return_value.start.side_effect = \
        MockedTraceableException

    scheduler_instance_with_mocks.start()

    mocked_sys_exit.called_once_with(127)
