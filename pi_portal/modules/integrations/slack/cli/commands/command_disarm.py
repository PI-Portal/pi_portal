"""Slack CLI Disarm command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import SlackProcessManagementCommandBase


class DisarmCommand(SlackProcessManagementCommandBase):
  """Slack CLI command to stop the camera process.

  :param client: The configured slack client to use.
  """

  process_name = ProcessList.CAMERA
  process_command: Literal["stop"] = "stop"
