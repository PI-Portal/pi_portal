"""Base process management class for Slack CLI commands."""

from pi_portal.modules.system.supervisor import SupervisorException
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcessException,
)
from typing_extensions import Literal
from .process_command import SlackProcessCommandBase


class SlackProcessManagementCommandBase(SlackProcessCommandBase):
  """A base command for the Slack CLI that manages a process.

  :param bot: The configured slack bot in use.
  """

  process_command: Literal["start", "stop"]
  process_notifier: Literal["start", "stop"]

  def hook_invoker(self) -> None:
    """Manage the configured process."""

    controller_command = getattr(self.process, self.process_command)
    controller_command()
    notifier_command = getattr(self.notifier, f"notify_{self.process_command}")
    notifier_command()

  def hook_supervisor_exception(self) -> None:
    """Handle a SupervisorException."""

    self.notifier.notify_error()

  def hook_supervisor_process_exception(self) -> None:
    """Handle a SupervisorProcessException."""

    notifier_command = getattr(
        self.notifier, f"notify_already_{self.process_command}"
    )
    notifier_command()

  def invoke(self) -> None:
    """Manage the process with error handling."""

    try:
      self.hook_invoker()
    except SupervisorProcessException:
      self.hook_supervisor_process_exception()
    except SupervisorException:
      self.hook_supervisor_exception()
