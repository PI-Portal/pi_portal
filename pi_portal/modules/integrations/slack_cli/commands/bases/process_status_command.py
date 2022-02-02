"""Base class for Slack CLI commands."""

from typing import Optional

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .process_command import ProcessCommandBase


class ProcessStatusCommandBase(ProcessCommandBase):
  """A base command for the Slack CLI that retrieves process information."""

  process_name: ProcessList
  process_command: Literal["status", "uptime"]
  result: Optional[str]

  def hook_invoker(self) -> None:
    """Retrieve process information."""

    status_command = getattr(self.process, self.process_command)
    self.result = status_command()
