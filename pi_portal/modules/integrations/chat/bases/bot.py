"""Chat integration chatbot base class."""

import abc
from typing import TYPE_CHECKING, Generic, TypeVar, cast

from pi_portal import config
from pi_portal.modules.integrations.chat import cli
from pi_portal.modules.mixins import write_archived_log_file
from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Mapping

  from typing_extensions import TypeAlias
  from .config import ChatConfigurationBase

TypeChatBot: "TypeAlias" = "ChatBotBase[Any]"

TypeIntegrationConfig = TypeVar(
    "TypeIntegrationConfig",
    bound="Mapping[str, Any]",
)


class ChatBotBase(
    write_archived_log_file.ArchivedLogFileWriter,
    Generic[TypeIntegrationConfig],
):
  """Chat integration chatbot base class."""

  configuration: "ChatConfigurationBase[TypeIntegrationConfig]"
  logger_name = "bot"
  log_file_path = config.LOG_FILE_CHAT_BOT

  def __init__(self) -> None:
    self.configure_logger()
    self.command_list = cli.get_available_commands()
    self.task_scheduler_client = TaskSchedulerServiceClient()

  @abc.abstractmethod
  def halt(self) -> None:
    """Stop the chatbot."""

  @abc.abstractmethod
  def start(self) -> None:
    """Start the chatbot."""

  def handle_command(self, command: str) -> None:
    """Handle a CLI command by name.

    :param command: The chat CLI command to handle.
    """

    self.log.debug("Received command: '%s'", command)
    if command in self.command_list:
      self.log.info("Executing valid command: '%s'", command)
      command_handler = cli.handler.ChatCLICommandHandler(
          bot=cast(TypeChatBot, self)
      )
      getattr(command_handler, command_handler.method_prefix + command)()
