"""Base process command class for Slack CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.modules.system.supervisor import SupervisorException
from pi_portal.modules.system.supervisor_config import ProcessList
from pi_portal.modules.system.supervisor_process import SupervisorProcess
from .command import CommandBase

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import Client  # pragma: no cover


class ProcessCommandBase(CommandBase, abc.ABC):
  """A base command for interacting with processes via the Slack CLI.

  :param client: The configured slack client to use.
  """

  process_name: ProcessList

  def __init__(self, client: "Client") -> None:
    super().__init__(client)
    self.process = SupervisorProcess(self.process_name)

  @abc.abstractmethod
  def hook_invoker(self) -> None:
    """Manage the configured process."""

  def hook_supervisor_exception(self) -> None:
    """Handle a SupervisorException."""

    self.notifier.notify_error()

  def invoke(self) -> None:
    """Manage the process with error handling."""

    try:
      self.hook_invoker()
    except SupervisorException:
      self.hook_supervisor_exception()
