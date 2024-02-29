"""Test fixtures for the processor mixins classes."""
import logging
from typing import Type

import pytest
from pi_portal.modules.tasks.processor.mixins.archival_client import (
    ArchivalClientMixin,
)
from pi_portal.modules.tasks.processor.mixins.camera_client import (
    CameraClientMixin,
)
from pi_portal.modules.tasks.processor.mixins.chat_client import ChatClientMixin

# pylint: disable=redefined-outer-name


@pytest.fixture
def concrete_archival_processor_mixin_class() -> Type[ArchivalClientMixin]:

  class ConcreteProcessor(ArchivalClientMixin):
    pass

  return ConcreteProcessor


@pytest.fixture
def concrete_archival_mixin_instance(
    concrete_archival_processor_mixin_class: Type[ArchivalClientMixin],
) -> ArchivalClientMixin:
  return concrete_archival_processor_mixin_class()


@pytest.fixture
def concrete_camera_processor_mixin_class() -> Type[CameraClientMixin]:

  class ConcreteProcessorBase:

    def __init__(self, log: logging.Logger):
      self.log = log

  class ConcreteProcessor(CameraClientMixin, ConcreteProcessorBase):
    pass

  return ConcreteProcessor


@pytest.fixture
def concrete_camera_mixin_instance(
    concrete_camera_processor_mixin_class: Type[ChatClientMixin],
    mocked_task_logger: logging.Logger,
) -> ChatClientMixin:
  return concrete_camera_processor_mixin_class(mocked_task_logger)


@pytest.fixture
def concrete_chat_processor_mixin_class() -> Type[ChatClientMixin]:

  class ConcreteProcessor(ChatClientMixin):
    pass

  return ConcreteProcessor


@pytest.fixture
def concrete_chat_mixin_instance(
    concrete_chat_processor_mixin_class: Type[ChatClientMixin],
) -> ChatClientMixin:
  return concrete_chat_processor_mixin_class()
