"""Slack CLI Arm command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import SlackProcessManagementCommandBase


class ArmCommand(SlackProcessManagementCommandBase):
  """Slack CLI command to start the camera process.

  :param bot: The configured slack bot in use.
  """

  process_name = ProcessList.CAMERA
  process_command: Literal["start"] = "start"
