"""DeadManSwitchCronJob class."""

from pi_portal import config
from ..bases import job


class DeadManSwitchCronJob(job.CronJobBase):
  """Logs a status message for external monitoring."""

  interval = config.CRON_INTERVAL_DEAD_MAN_SWITCH
  name = "Dead Man's Switch"

  def cron(self) -> None:
    """Cron implementation."""

    self.log.info(
        "ok",
        extra={"job": self.name},
    )
