"""Test the CronJobBase class."""

import logging
from io import StringIO
from unittest import mock

import pytest
from .. import job


class Interrupt(Exception):
  """Raised to interrupt the cron job during testing."""


class TestCronJobBase:
  """Test the CronJobBase class."""

  def test__initialization__attributes(
      self,
      concrete_cron_instance: job.CronJobBase,
      mocked_interval: int,
      mocked_cron_logger: logging.Logger,
  ) -> None:
    assert concrete_cron_instance.interval == mocked_interval
    assert concrete_cron_instance.log == mocked_cron_logger
    assert concrete_cron_instance.name == "mock_cron_job"

  def test__initialization__inheritance(
      self,
      concrete_cron_instance: job.CronJobBase,
  ) -> None:
    assert isinstance(
        concrete_cron_instance,
        job.CronJobBase,
    )

  def test__start__single_run__sleep(
      self,
      concrete_cron_instance: job.CronJobBase,
      mocked_sleep: mock.Mock,
  ) -> None:
    mocked_sleep.side_effect = Interrupt

    with pytest.raises(Interrupt):
      concrete_cron_instance.start()

    mocked_sleep.assert_called_once_with(concrete_cron_instance.interval)

  def test__start__single_run__logging(
      self,
      concrete_cron_instance: job.CronJobBase,
      mocked_sleep: mock.Mock,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    mocked_sleep.side_effect = Interrupt
    cron_job_name = concrete_cron_instance.name

    with pytest.raises(Interrupt):
      concrete_cron_instance.start()

    assert mocked_cron_logger_stream.getvalue() == (
        f"WARNING - {cron_job_name} - Cron job '{cron_job_name}' "
        f"is starting ...\n"
        f"INFO - {cron_job_name} - Cron method has been called.\n"
    )

  def test__start__two_runs__sleep(
      self,
      concrete_cron_instance: job.CronJobBase,
      mocked_sleep: mock.Mock,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      concrete_cron_instance.start()

    assert mocked_sleep.mock_calls == [
        mock.call(concrete_cron_instance.interval),
        mock.call(concrete_cron_instance.interval),
    ]

  def test__start__two_runs__logging(
      self,
      concrete_cron_instance: job.CronJobBase,
      mocked_sleep: mock.Mock,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]
    cron_job_name = concrete_cron_instance.name

    with pytest.raises(Interrupt):
      concrete_cron_instance.start()

    assert mocked_cron_logger_stream.getvalue() == (
        f"WARNING - {cron_job_name} - Cron job '{cron_job_name}' "
        f"is starting ...\n"
        f"INFO - {cron_job_name} - Cron method has been called.\n"
        f"INFO - {cron_job_name} - Cron method has been called.\n"
    )
