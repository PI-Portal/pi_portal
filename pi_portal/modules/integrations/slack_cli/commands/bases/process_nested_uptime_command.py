"""Base process uptime command that can be nested within other commands."""

from pi_portal.modules.system import supervisor
from typing_extensions import Literal
from .process_status_command import ProcessStatusCommandBase


class NestedUptimeCommandBase(ProcessStatusCommandBase):
  """Retrieves uptime for the process and re-raises supervisor exceptions."""

  process_command: Literal["uptime"] = "uptime"

  def hook_supervisor_exception(self) -> None:
    """Re-raise the SupervisorException.

    :raises: :class:`supervisor.SupervisorException`
    """
    super().hook_supervisor_exception()
    raise supervisor.SupervisorException("Unknown error!")
