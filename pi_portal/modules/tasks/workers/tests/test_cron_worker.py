"""Test the CronWorker class."""
import logging
from concurrent.futures import Future
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.modules.python.futures import wait_cm
from pi_portal.modules.tasks.conftest import Interrupt
from pi_portal.modules.tasks.workers.bases.worker_base import WorkerBase
from pi_portal.modules.tasks.workers.cron_jobs.bases.cron_job_base import (
    CronJobAlarm,
)
from .. import cron_worker


class TestCronWorker:
  """Test the CronWorker class."""

  logging_start_up_message = (
      "WARNING - None - Scheduler - None - "
      "Loading cron job '{mocked_cron_job_1.CronJobClass.name}' ...\n"
      "WARNING - None - Scheduler - None - "
      "Loading cron job '{mocked_cron_job_2.CronJobClass.name}' ...\n"
      "WARNING - None - Scheduler - None - Cron scheduler is starting ...\n"
  )

  def test_initialize__cron_jobs(
      self,
      cron_worker_instance: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
      mocked_worker_logger: logging.Logger,
      mocked_task_registry: mock.Mock,
  ) -> None:
    for index, mocked_cron_job in enumerate(mocked_task_registry_cron_jobs):
      mocked_cron_job.CronJobClass.assert_called_once_with(
          mocked_worker_logger,
          mocked_task_registry,
      )
      assert cron_worker_instance.jobs[index] == \
          mocked_cron_job.CronJobClass.return_value

  def test_initialize__logger(
      self,
      cron_worker_instance: cron_worker.CronWorker,
      mocked_worker_logger: logging.Logger,
  ) -> None:
    assert cron_worker_instance.log == mocked_worker_logger
    assert isinstance(
        cron_worker_instance.log,
        logging.Logger,
    )

  def test_initialize__task_router(
      self,
      cron_worker_instance: cron_worker.CronWorker,
      mocked_task_router: mock.Mock,
  ) -> None:
    assert cron_worker_instance.router == mocked_task_router

  def test_initialize__inheritance(
      self,
      cron_worker_instance: cron_worker.CronWorker,
  ) -> None:
    assert isinstance(cron_worker_instance, WorkerBase)

  def test_start__single_run__logging(
      self,
      cron_worker_instance_single_run: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    with pytest.raises(Interrupt):
      cron_worker_instance_single_run.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message.format(
        mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
        mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
    )

  def test_start__single_run__calls_tick(
      self,
      cron_worker_instance_single_run: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_single_run.jobs = mocked_task_registry_cron_jobs

    with pytest.raises(Interrupt):
      cron_worker_instance_single_run.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      mocked_job.tick.assert_called_once_with()

  def test_start__single_run__does_not_call_schedule(
      self,
      cron_worker_instance_single_run: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:

    with pytest.raises(Interrupt):
      cron_worker_instance_single_run.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      mocked_job.schedule.assert_not_called()

  def test_start__single_run__calls_sleep(
      self,
      cron_worker_instance_single_run: cron_worker.CronWorker,
      mocked_sleep: mock.Mock,
  ) -> None:
    with pytest.raises(Interrupt):
      cron_worker_instance_single_run.start()

    assert mocked_sleep.mock_calls == [mock.call(1)] * (1 + 1)

  def test_start__two_runs__logging(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message.format(
        mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
        mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
    )

  def test_start__two_runs__does_not_call_schedule(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      mocked_job.schedule.assert_not_called()

  def test_start__two_runs__calls_sleep(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_sleep: mock.Mock,
  ) -> None:
    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_sleep.mock_calls == [mock.call(1)] * (2 + 1)

  def test_start__two_runs__calls_tick(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      assert mocked_job.tick.mock_calls == [mock.call()] * 2

  def test_start__two_runs__schedules_a_job__logging__quiet(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]
    mocked_task_registry_cron_jobs[1].quiet = True

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message.format(
        mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
        mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
    )

  def test_start__two_runs__schedules_a_job__logging__not_quiet__(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]
    mocked_task_registry_cron_jobs[1].quiet = False

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message.format(
        mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
        mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
    ) + (
        "INFO - None - Scheduler - None - Scheduling the "
        f"'{mocked_task_registry_cron_jobs[1].name}' cron job.\n"
    )

  def test_start__two_runs__schedules_a_job__calls_tick(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      assert mocked_job.tick.mock_calls == [mock.call()] * 2

  def test_start__two_runs__schedules_a_job__calls_schedule(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_router: mock.Mock,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    mocked_task_registry_cron_jobs[1].schedule.assert_called_once_with(
        mocked_task_router
    )

  def test_start__two_runs__schedules_a_job__calls_sleep(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
      mocked_sleep: mock.Mock,
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_sleep.mock_calls == [mock.call(1)] * (2 + 1)

  def test_start__two_runs__schedules_a_job__exception__logging__quiet(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]
    mocked_task_registry_cron_jobs[1].schedule.side_effect = Exception
    mocked_task_registry_cron_jobs[1].quiet = True

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_stream.getvalue().startswith(
        self.logging_start_up_message.format(
            mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
            mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
        ) + (
            f"ERROR - None - {mocked_task_registry_cron_jobs[1].name} - None - "
            f"A scheduled '{mocked_task_registry_cron_jobs[1].name}' cron job "
            "encountered a critical failure!\n"
            f"ERROR - None - {mocked_task_registry_cron_jobs[1].name} - "
            "None - Exception\n"
        )
    )
    assert mocked_stream.getvalue().endswith("Exception\n")

  def test_start__two_runs__schedules_a_job__exception__logging__not_quiet(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]
    mocked_task_registry_cron_jobs[1].schedule.side_effect = Exception
    mocked_task_registry_cron_jobs[1].quiet = False

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_stream.getvalue().startswith(
        self.logging_start_up_message.format(
            mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
            mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
        ) + (
            "INFO - None - Scheduler - None - Scheduling the "
            f"'{mocked_task_registry_cron_jobs[1].name}' cron job.\n"
            f"ERROR - None - {mocked_task_registry_cron_jobs[1].name} - None - "
            f"A scheduled '{mocked_task_registry_cron_jobs[1].name}' cron job "
            "encountered a critical failure!\n"
            f"ERROR - None - {mocked_task_registry_cron_jobs[1].name} - "
            "None - Exception\n"
        )
    )
    assert mocked_stream.getvalue().endswith("Exception\n")

  def test_start__two_runs__schedules_a_job__exception__calls_tick(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    for mocked_job in mocked_task_registry_cron_jobs:
      assert mocked_job.tick.mock_calls == [mock.call()] * 2

  def test_start__two_runs__schedules_a_job__exception__calls_schedule(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_router: mock.Mock,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    mocked_task_registry_cron_jobs[1].schedule.assert_called_once_with(
        mocked_task_router
    )

  def test_start__two_runs__schedules_a_job__exception__calls_sleep(
      self,
      cron_worker_instance_two_runs: cron_worker.CronWorker,
      mocked_task_registry_cron_jobs: List[mock.Mock],
      mocked_sleep: mock.Mock,
  ) -> None:
    cron_worker_instance_two_runs.jobs = mocked_task_registry_cron_jobs
    mocked_task_registry_cron_jobs[1].tick.side_effect = [None, CronJobAlarm]

    with pytest.raises(Interrupt):
      cron_worker_instance_two_runs.start()

    assert mocked_sleep.mock_calls == [mock.call(1)] * (2 + 1)

  def test_halt__server_is_running__logging(
      self,
      cron_worker_running: "Future[None]",
      cron_worker_instance: cron_worker.CronWorker,
      mocked_stream: StringIO,
      mocked_task_registry_cron_jobs: List[mock.Mock],
  ) -> None:
    with wait_cm(cron_worker_running):
      cron_worker_instance.halt()

    assert mocked_stream.getvalue() == self.logging_start_up_message.format(
        mocked_cron_job_1=mocked_task_registry_cron_jobs[0],
        mocked_cron_job_2=mocked_task_registry_cron_jobs[1],
    ) + (
        "WARNING - None - Scheduler - None - "
        "Cron scheduler is shutting down ...\n"
    )

  def test_halt__server_is_running__stops_server(
      self,
      cron_worker_running: "Future[None]",
      cron_worker_instance: cron_worker.CronWorker,
  ) -> None:
    with wait_cm(cron_worker_running):
      cron_worker_instance.halt()

  def test_halt__server_is_running__ensure_minimum_iterations(
      self,
      cron_worker_running: "Future[None]",
      cron_worker_instance: cron_worker.CronWorker,
      mocked_sleep: mock.Mock,
  ) -> None:
    with wait_cm(cron_worker_running):
      cron_worker_instance.halt()

    assert mocked_sleep.call_count > 10
