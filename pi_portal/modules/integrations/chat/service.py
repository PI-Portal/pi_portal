"""The chatbot service."""

from typing import Type

from .bases.bot import TypeChatBot
from .slack.bot import SlackBot

ChatBot: Type[TypeChatBot] = SlackBot
