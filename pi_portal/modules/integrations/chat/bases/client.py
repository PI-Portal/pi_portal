"""Chat integration chat client base class."""

import abc
from typing import TYPE_CHECKING, Generic, TypeVar

from pi_portal import config
from pi_portal.modules.mixins import write_archived_log_file

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Mapping

  from typing_extensions import TypeAlias
  from .config import ChatConfigurationBase

TypeChatClient: "TypeAlias" = "ChatClientBase[Any]"

TypeIntegrationConfig = TypeVar(
    "TypeIntegrationConfig",
    bound="Mapping[str, Any]",
)


class ChatClientError(Exception):
  """Raised when the chat client implementation encounters an error."""


class ChatClientBase(
    write_archived_log_file.ArchivedLogFileWriter,
    Generic[TypeIntegrationConfig],
):
  """Chat integration chat messaging client."""

  configuration: "ChatConfigurationBase[TypeIntegrationConfig]"
  log_file_path = config.LOG_FILE_CHAT_CLIENT
  logger_name = "client"

  def __init__(self, propagate_exceptions: bool) -> None:
    self.configure_logger()
    self.propagate_exceptions = propagate_exceptions

  @abc.abstractmethod
  def send_message(self, message: str) -> None:
    """Send a message to the chat server.

    Implementations must handle raised exceptions and log errors appropriately.

    :param message: The message to send to chat.
    :raises: :class:`ChatClientError`
    """

  @abc.abstractmethod
  def send_file(self, file_name: str, description: str) -> None:
    """Send a file to the chat server.

    Implementations must handle raised exceptions and log errors appropriately.

    :param file_name: The path to upload to the chat server.
    :param description: A description of the file being uploaded.
    :raises: :class:`ChatClientError`
    """
