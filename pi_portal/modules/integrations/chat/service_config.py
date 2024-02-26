"""The chat service configuration."""

from typing import Type

from .bases.config import TypeChatConfig
from .slack.config import SlackIntegrationConfiguration

ChatConfig: Type[TypeChatConfig] = SlackIntegrationConfiguration
