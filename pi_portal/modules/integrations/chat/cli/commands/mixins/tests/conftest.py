"""Test fixtures for the chat CLI mixin classes."""
import pytest
from .. import task_scheduler_client


@pytest.fixture
def concrete_task_scheduler_client_mixin_instance(
) -> task_scheduler_client.TaskSchedulerClientMixin:

  class ConcreteCommand(task_scheduler_client.TaskSchedulerClientMixin):
    pass

  return ConcreteCommand()
