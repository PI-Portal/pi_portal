"""Configuration for the chat integration client."""

from typing import TYPE_CHECKING, Generic, TypeVar

from pi_portal.modules.configuration import state

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Mapping

  from typing_extensions import TypeAlias

TypeChatConfig: "TypeAlias" = "ChatConfigurationBase[Any]"

TypeSettings = TypeVar("TypeSettings", bound="Mapping[str, Any]")


class ChatConfigurationBase(Generic[TypeSettings]):
  """Configuration for the chat integration."""

  current_state: state.State
  settings: TypeSettings
  emoji_alert: str

  def __init__(self) -> None:
    self.current_state = state.State()
