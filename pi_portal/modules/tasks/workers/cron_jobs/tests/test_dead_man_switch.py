"""Test the dead_man_switch module."""
import logging
from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.mixins import write_unarchived_log_file
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from .. import dead_man_switch
from ..bases import cron_job_base


class TestDadManSwitchLogger:
  """Test the DeadManSwitchLogger class."""

  def test_initialize__attributes(
      self,
      dead_man_switch_logger_instance: dead_man_switch.DeadManSwitchLogger,
      mocked_worker_logger: logging.Logger,
  ) -> None:
    assert dead_man_switch_logger_instance.log == mocked_worker_logger
    assert dead_man_switch_logger_instance.logger_name == "dead_man_switch"
    assert dead_man_switch_logger_instance.log_file_path == (
        config.LOG_FILE_DEAD_MAN_SWITCH
    )

  def test_initialize__inheritance(
      self,
      dead_man_switch_logger_instance: dead_man_switch.DeadManSwitchLogger,
  ) -> None:
    assert isinstance(
        dead_man_switch_logger_instance,
        write_unarchived_log_file.UnarchivedLogFileWriter,
    )


class TestDeadManSwitchCronJob:
  """Test the dead_man_switch module."""

  def test_initialize__attributes(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    assert dead_man_switch_cron_job_instance.interval == \
        config.CRON_INTERVAL_DEAD_MAN_SWITCH
    assert dead_man_switch_cron_job_instance.name == "Dead Man's Switch"
    assert dead_man_switch_cron_job_instance.quiet is True
    assert dead_man_switch_cron_job_instance.type == \
        enums.TaskType.NON_SCHEDULED

  def test_initialize__inheritance(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    assert isinstance(
        dead_man_switch_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_initialize__isolated_logger(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    assert isinstance(
        dead_man_switch_cron_job_instance.isolated_logger,
        dead_man_switch.DeadManSwitchLogger,
    )

  def test_args__returns_correct_value(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    expected_args = non_scheduled.Args()

    # pylint: disable=protected-access
    assert dead_man_switch_cron_job_instance._args() == expected_args

  def test_hook_submit__standard_logging(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    dead_man_switch_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == ""

  def test_hook_submit__isolated_logging(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
      mocked_task_scheduler: mock.Mock,
      mocked_isolated_stream: StringIO,
  ) -> None:
    dead_man_switch_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_isolated_stream.getvalue() == \
        "INFO - None - Dead Man's Switch - None - ok\n"
