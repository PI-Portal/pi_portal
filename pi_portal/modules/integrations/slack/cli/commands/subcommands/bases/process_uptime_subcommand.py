"""Base chat CLI process uptime subcommand."""

from pi_portal.modules.system import supervisor
from typing_extensions import Literal
from ...bases.process_status_command import ChatProcessStatusCommandBase


class ChatProcessUptimeCommandBase(ChatProcessStatusCommandBase):
  """Retrieves uptime for the process and re-raises supervisor exceptions."""

  process_command: Literal["uptime"] = "uptime"
  supervisor_exception_message = "Unknown supervisord error!"

  def hook_supervisor_exception(self) -> None:
    """Re-raise the SupervisorException.

    :raises: :class:`supervisor.SupervisorException`
    """
    super().hook_supervisor_exception()
    raise supervisor.SupervisorException(self.supervisor_exception_message)
