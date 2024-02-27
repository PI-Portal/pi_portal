"""Machine CLI command to start the task scheduler service."""

import uvicorn
from pi_portal import config
from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import state


class TaskSchedulerCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the task scheduler service."""

  def invoke(self) -> None:
    """Invoke the command."""

    uvicorn.run(
        "pi_portal.modules.tasks:create_service",
        factory=True,
        uds=config.PI_PORTAL_TASK_MANAGER_SOCKET,
        reload=False,
        workers=1,
        limit_concurrency=2,
    )
