"""Base class for chat CLI commands."""

from typing import TYPE_CHECKING, Optional

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .process_command import ChatProcessCommandBase

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.integrations.chat import TypeChatBot


class ChatProcessStatusCommandBase(ChatProcessCommandBase):
  """A base command for the chat CLI that retrieves process information.

  :param bot: The configured chatbot in use.
  """

  process_name: ProcessList
  process_command: Literal["status", "uptime"]
  result: Optional[str]

  def __init__(self, bot: "TypeChatBot") -> None:
    super().__init__(bot)
    self.result = None

  def hook_invoker(self) -> None:
    """Retrieve process information."""

    status_command = getattr(self.process, self.process_command)
    self.result = status_command()
