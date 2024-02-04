"""Test fixtures for the processor mixins classes."""
# pylint: disable=redefined-outer-name

from typing import Type

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks.processor.mixins.archival_client import (
    ArchivalClientMixin,
)
from pi_portal.modules.tasks.processor.mixins.chat_client import ChatClientMixin


@pytest.fixture
def concrete_archival_processor_mixin_class() -> Type[ArchivalClientMixin]:

  class ConcreteProcessor(ArchivalClientMixin):
    pass

  return ConcreteProcessor


@pytest.fixture
def concrete_archival_mixin_instance(
    concrete_archival_processor_mixin_class: Type[ArchivalClientMixin],
    mocked_state: state.State,
) -> ArchivalClientMixin:
  state.State().user_config = mocked_state.user_config
  return concrete_archival_processor_mixin_class()


@pytest.fixture
def concrete_chat_processor_mixin_class() -> Type[ChatClientMixin]:

  class ConcreteProcessor(ChatClientMixin):
    pass

  return ConcreteProcessor


@pytest.fixture
def concrete_chat_mixin_instance(
    concrete_chat_processor_mixin_class: Type[ChatClientMixin],
    mocked_state: state.State,
) -> ChatClientMixin:
  state.State().user_config = mocked_state.user_config
  return concrete_chat_processor_mixin_class()
