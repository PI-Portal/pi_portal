"""Base class for Slack CLI commands."""

from typing import Optional

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .process_command import SlackProcessCommandBase


class SlackProcessStatusCommandBase(SlackProcessCommandBase):
  """A base command for the Slack CLI that retrieves process information.

  :param bot: The configured slack bot in use.
  """

  process_name: ProcessList
  process_command: Literal["status", "uptime"]
  result: Optional[str]

  def hook_invoker(self) -> None:
    """Retrieve process information."""

    status_command = getattr(self.process, self.process_command)
    self.result = status_command()
