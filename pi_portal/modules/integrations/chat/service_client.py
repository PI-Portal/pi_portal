"""The chat service client."""

from typing import Type

from .bases.client import TypeChatClient
from .slack.client import SlackClient

ChatClient: Type[TypeChatClient] = SlackClient
