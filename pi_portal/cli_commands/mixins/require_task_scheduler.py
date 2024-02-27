"""CommandBase mixin to ensure the task scheduler is running."""

import click
from pi_portal import config
from pi_portal.modules.system import file_system


class CommandTaskSchedulerMixin:
  """CommandBase mixin to ensure the task scheduler is running."""

  def require_task_scheduler(self) -> None:
    """Wait until the task manager service is running."""

    click.echo("Waiting for task manager service ... ", nl=False)
    socket = file_system.FileSystem(config.PI_PORTAL_TASK_MANAGER_SOCKET)
    socket.wait_until_exists()
    click.echo("Ready!")
