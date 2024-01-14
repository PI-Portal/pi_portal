"""Test the CronSchedulerCommand class."""

from unittest import mock

from .. import cron_scheduler
from ..bases import command
from ..mixins import state


class TestCronSchedulerCommand:
  """Test the CronSchedulerCommand class."""

  def test_initialize__inheritance(
      self,
      cron_instance: cron_scheduler.CronSchedulerCommand,
  ) -> None:
    assert isinstance(cron_instance, command.CommandBase)
    assert isinstance(
        cron_instance,
        state.CommandManagedStateMixin,
    )

  def test_invoke__calls(
      self,
      cron_instance: cron_scheduler.CronSchedulerCommand,
      mocked_cron_scheduler: mock.Mock,
  ) -> None:
    cron_instance.invoke()

    mocked_cron_scheduler.assert_called_once_with()
    mocked_cron_scheduler.return_value.start.assert_called_once_with()
