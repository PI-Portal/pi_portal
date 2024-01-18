"""Test the dead_man_switch module."""

from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from .. import dead_man_switch
from ..bases import cron_job_base


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
    assert dead_man_switch_cron_job_instance.priority == \
        enums.TaskPriority.STANDARD

  def test_initialize__inheritance(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    assert isinstance(
        dead_man_switch_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
  ) -> None:
    expected_args = non_scheduled.Args()

    # pylint: disable=protected-access
    assert dead_man_switch_cron_job_instance._args() == expected_args

  def test_hook_submit__logging(
      self,
      dead_man_switch_cron_job_instance: dead_man_switch.CronJob,
      mocked_queue: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    dead_man_switch_cron_job_instance.schedule(mocked_queue)

    assert mocked_stream.getvalue() == \
        "INFO - None - Dead Man's Switch - None - ok\n"
