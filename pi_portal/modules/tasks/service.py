"""The task scheduler service."""

from pi_portal.modules.tasks.api.server import Server
from pi_portal.modules.tasks.scheduler import TaskScheduler


class TaskSchedulerService:
  """The task scheduler service."""

  def __init__(self) -> None:
    self.scheduler = TaskScheduler()
    self.server = Server(self.scheduler)
