"""Test the DeadManSwitchCronJob class."""
import logging
from io import StringIO

from pi_portal import config
from ...bases import job
from .. import dead_man_switch


class TestDeadManSwitchCronJob:
  """Test the DeadManSwitchCronJob class."""

  def test__initialization__attrs(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.DeadManSwitchCronJob,
      mocked_cron_logger: logging.Logger
  ) -> None:
    assert dead_man_switch_cron_job_instance.interval == \
           config.CRON_INTERVAL_DEAD_MAN_SWITCH
    assert dead_man_switch_cron_job_instance.log == \
           mocked_cron_logger
    assert dead_man_switch_cron_job_instance.name == \
           "Dead Man's Switch"

  def test__initialization__inheritance(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.DeadManSwitchCronJob,
  ) -> None:
    assert isinstance(
        dead_man_switch_cron_job_instance,
        job.CronJobBase,
    )

  def test__cron__logging(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.DeadManSwitchCronJob,
      mocked_cron_logger_stream: StringIO,
  ) -> None:
    dead_man_switch_cron_job_instance.cron()

    assert mocked_cron_logger_stream.getvalue() == \
        "INFO - Dead Man's Switch - ok\n"
