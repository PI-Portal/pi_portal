"""CLI command to start the cron scheduler."""

from pi_portal.modules.cron import scheduler
from .bases import command
from .mixins import state


class CronSchedulerCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the cron scheduler."""

  def invoke(self) -> None:
    """Invoke the command."""

    cron = scheduler.CronScheduler()
    cron.start()
